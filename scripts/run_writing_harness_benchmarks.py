#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

from writing_checks import (
    build_default_cw_artifact,
    count_any,
    count_phrase,
    cw_artifact_path_for_candidate,
    evaluate_cognitive_dimensions,
    evaluate_genre_contract,
    evaluate_module_coverage,
    lint_writing,
    load_cw_artifact_if_present,
    load_trace_if_present,
    read_text as read,
    summarize_lint,
    validate_cw_artifact,
    validate_trace_payload,
    word_count,
)

ROOT = Path(__file__).resolve().parent.parent
BENCH_DIR = ROOT / "evals" / "benchmarks"
CASES_PATH = BENCH_DIR / "cases.json"
GOLD_DIR = BENCH_DIR / "gold"
REPORTS_DIR = ROOT / "evals" / "reports"


@dataclass
class Metric:
    name: str
    points: int
    earned: float
    detail: str


@dataclass
class CaseReport:
    case_id: str
    mode: str
    score: float
    max_score: int
    metrics: list[Metric]


def load_cases() -> list[dict]:
    return json.loads(read(CASES_PATH))


def metric_from_checks(name: str, points: int, checks: list, success_detail: str) -> Metric:
    failed_errors = [check for check in checks if not check.passed and check.severity == "error"]
    failed_all = [check for check in checks if not check.passed]
    if not checks:
        return Metric(name, points, points, success_detail)
    if failed_errors:
        earned = 0
    else:
        earned = round(points * ((len(checks) - len(failed_all)) / len(checks)), 2)
    detail = success_detail if not failed_all else f"failed: {', '.join(check.name for check in failed_all[:4])}"
    return Metric(name, points, earned, detail)


def score_case(case: dict, candidate: str, mode: str, candidate_path: Path | None = None) -> CaseReport:
    input_text = case["input_text"]
    metrics: list[Metric] = []
    cw_artifact = load_cw_artifact_if_present(candidate_path) if candidate_path is not None else None

    wc = word_count(candidate)
    min_words = case["target_words"]["min"]
    max_words = case["target_words"]["max"]
    if min_words <= wc <= max_words:
        metrics.append(Metric("word_count_fit", 10, 10, f"{wc} words"))
    else:
        metrics.append(Metric("word_count_fit", 10, 0, f"{wc} words, target {min_words}-{max_words}"))

    preserve = case["preserve_facts_all"]
    preserve_hits = count_any(candidate, preserve)
    preserve_score = 20 * (preserve_hits / len(preserve))
    metrics.append(Metric("fact_preservation", 20, preserve_score, f"{preserve_hits}/{len(preserve)} preserved"))

    strengthen = case["strengthen_with_any"]
    strengthen_hits = count_any(candidate, strengthen)
    strengthen_score = 20 * min(strengthen_hits / 2, 1.0)
    metrics.append(Metric("strengthening_signals", 20, strengthen_score, f"{strengthen_hits} strengthening signals"))

    avoid = case["avoid_phrases"]
    avoid_hits = count_any(candidate, avoid)
    avoid_score = 15 * max(0.0, 1.0 - (avoid_hits / max(len(avoid), 1)))
    metrics.append(Metric("banned_phrase_removal", 15, avoid_score, f"{avoid_hits} banned phrases present"))

    reductions = case["reduce_phrases"]
    improved = 0
    for phrase in reductions:
        if count_phrase(candidate, phrase) < count_phrase(input_text, phrase):
            improved += 1
    reduction_score = 15 * (improved / len(reductions))
    metrics.append(Metric("weak_pattern_reduction", 15, reduction_score, f"{improved}/{len(reductions)} reduced"))

    judgment = case["judgment_markers_any"]
    judgment_hits = count_any(candidate, judgment)
    judgment_score = 10 if judgment_hits > 0 else 0
    metrics.append(Metric("judgment_markers", 10, judgment_score, f"{judgment_hits} judgment markers"))

    specificity = case["specificity_markers_any"]
    specificity_hits = count_any(candidate, specificity)
    specificity_score = 10 * min(specificity_hits / 2, 1.0)
    metrics.append(Metric("specificity_markers", 10, specificity_score, f"{specificity_hits} specificity markers"))

    lint_summary = summarize_lint(lint_writing(candidate))
    lint_score = round((lint_summary["score"] / 100) * 10, 2)
    metrics.append(
        Metric(
            "writing_lint",
            10,
            lint_score,
            "pass" if lint_summary["passed"] else f"failed: {', '.join(lint_summary['failed_checks'])}",
        )
    )

    contract_checks = evaluate_genre_contract(case, candidate)
    contract_failed = [check for check in contract_checks if not check.passed]
    contract_score = 10 * ((len(contract_checks) - len(contract_failed)) / len(contract_checks)) if contract_checks else 10
    metrics.append(
        Metric(
            "genre_contracts",
            10,
            round(contract_score, 2),
            "all contracts met" if not contract_failed else f"failed: {', '.join(check.name for check in contract_failed)}",
        )
    )

    cognitive_checks = evaluate_cognitive_dimensions(case, candidate, cw_artifact)
    metrics.append(metric_from_checks("cognitive_dimensions", 15, cognitive_checks, "K/P/A targets met"))

    artifact_checks = validate_cw_artifact(cw_artifact)
    metrics.append(metric_from_checks("cw_artifact", 10, artifact_checks, "cw artifact complete"))

    module_checks = evaluate_module_coverage(cw_artifact)
    metrics.append(metric_from_checks("module_coverage", 10, module_checks, "module spec coverage present"))

    trace_payload = load_trace_if_present(candidate_path) if candidate_path is not None else None
    trace_checks = validate_trace_payload(trace_payload)
    metrics.append(metric_from_checks("trace_completeness", 5, trace_checks, "trace present"))

    total = sum(metric.earned for metric in metrics)
    max_score = sum(metric.points for metric in metrics)
    return CaseReport(case_id=case["id"], mode=mode, score=round(total, 2), max_score=max_score, metrics=metrics)


def render_prompt_packet(case: dict) -> str:
    return f"""# Writing Harness Benchmark Prompt

Case ID: {case["id"]}
Title: {case["title"]}
Surface: {case["surface"]}
Audience: {case["audience"]}
Task: {case["task"]}

Rewrite requirements:
- Preserve these facts: {", ".join(case["preserve_facts_all"])}
- Strengthen with details such as: {", ".join(case["strengthen_with_any"])}
- Avoid these phrases: {", ".join(case["avoid_phrases"])}
- Reduce these weak patterns if present: {", ".join(case["reduce_phrases"])}
- Satisfy these genre contracts: {", ".join(contract["name"] for contract in case.get("genre_contracts", []))}
- Emit a CW artifact with baseline, architecture, modules, trace, unit tests, integration, and rollback.

Instructions:
Rewrite the draft for authored quality.
Do not optimize for casualness or fake humanity.
Optimize for clear intent, stronger judgment, audience awareness, concrete detail, and credible voice.

Draft:
{case["input_text"]}
"""


def evaluate_cases(cases: list[dict], mode: str, candidate_dir: Path | None = None) -> list[CaseReport]:
    reports: list[CaseReport] = []
    for case in cases:
        if mode == "gold":
            candidate_path = GOLD_DIR / f"{case['id']}.md"
            candidate = read(candidate_path)
        elif mode == "input":
            candidate = case["input_text"]
            candidate_path = None
        elif mode == "candidate":
            assert candidate_dir is not None
            candidate_path = candidate_dir / f"{case['id']}.md"
            candidate = read(candidate_path)
        else:
            raise ValueError(f"Unsupported mode: {mode}")
        reports.append(score_case(case, candidate, mode, candidate_path))
    return reports


def print_case_reports(reports: list[CaseReport], header: str) -> None:
    print(header)
    total = sum(report.score for report in reports)
    max_total = sum(report.max_score for report in reports)
    pct = round((total / max_total) * 100, 2) if max_total else 0.0
    print(f"Aggregate score: {total:.2f}/{max_total} ({pct}%)")
    for report in reports:
        print(f"  - {report.case_id}: {report.score:.2f}/{report.max_score}")


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate-dir")
    parser.add_argument("--use-gold", action="store_true")
    parser.add_argument("--use-input", action="store_true")
    parser.add_argument("--sanity", action="store_true")
    parser.add_argument("--json")
    parser.add_argument("--emit-prompts")
    args = parser.parse_args()

    cases = load_cases()

    if args.emit_prompts:
        out_dir = Path(args.emit_prompts)
        out_dir.mkdir(parents=True, exist_ok=True)
        for case in cases:
            (out_dir / f"{case['id']}.md").write_text(render_prompt_packet(case), encoding="utf-8")
            (out_dir / f"{case['id']}.cw.json").write_text(json.dumps(build_default_cw_artifact(case), indent=2), encoding="utf-8")
        print(f"Wrote prompt packets to {out_dir}")
        return 0

    if args.sanity:
        gold_reports = evaluate_cases(cases, "gold")
        input_reports = evaluate_cases(cases, "input")
        print_case_reports(gold_reports, "Gold Benchmark Run")
        print()
        print_case_reports(input_reports, "Raw Input Baseline")
        print()

        discriminative = all(g.score > i.score for g, i in zip(gold_reports, input_reports))
        margin = round(sum(g.score for g in gold_reports) - sum(i.score for i in input_reports), 2)
        print(f"Sanity result: {'PASS' if discriminative else 'FAIL'}")
        print(f"Gold-minus-input margin: {margin}")

        payload = {
            "mode": "sanity",
            "gold": [asdict(report) for report in gold_reports],
            "input": [asdict(report) for report in input_reports],
            "discriminative": discriminative,
            "margin": margin,
        }
        if args.json:
            write_json(Path(args.json), payload)
            print(f"Wrote JSON report to {args.json}")
        return 0 if discriminative else 1

    if args.use_gold:
        reports = evaluate_cases(cases, "gold")
        mode = "gold"
    elif args.use_input:
        reports = evaluate_cases(cases, "input")
        mode = "input"
    elif args.candidate_dir:
        reports = evaluate_cases(cases, "candidate", Path(args.candidate_dir))
        mode = "candidate"
    else:
        parser.error("Choose one of --sanity, --use-gold, --use-input, or --candidate-dir")

    print_case_reports(reports, f"Writing Harness Benchmark Run ({mode})")
    passed = all(report.score >= 70 for report in reports)
    print()
    print(f"Threshold result: {'PASS' if passed else 'FAIL'} (case threshold: 70/100)")

    payload = {
        "mode": mode,
        "passed": passed,
        "reports": [asdict(report) for report in reports],
    }
    if args.json:
        write_json(Path(args.json), payload)
        print(f"Wrote JSON report to {args.json}")

    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main())
