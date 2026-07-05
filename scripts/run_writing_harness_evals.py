#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parent.parent
README = ROOT / "README.md"
SKILL = ROOT / "skills" / "writing-harness" / "SKILL.md"
REF_DIR = ROOT / "skills" / "writing-harness" / "references"
CASES = ROOT / "evals" / "cases" / "behavioral-coverage.json"


@dataclass
class CheckResult:
    suite: str
    name: str
    passed: bool
    detail: str


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.lower()).strip()


def contains_all(text: str, terms: Iterable[str]) -> tuple[bool, list[str]]:
    haystack = normalize(text)
    missing = [term for term in terms if normalize(term) not in haystack]
    return not missing, missing


def artifact_checks() -> list[CheckResult]:
    results: list[CheckResult] = []

    readme = read(README)
    skill = read(SKILL)
    refs = {path.name: read(path) for path in REF_DIR.glob("*.md")}

    required_files = [
        README,
        SKILL,
        REF_DIR / "rewrite-workflow.md",
        REF_DIR / "rubric.md",
        REF_DIR / "failure-taxonomy.md",
        REF_DIR / "prompt-templates.md",
        REF_DIR / "cognitive-baseline.md",
        REF_DIR / "aeh-architecture.md",
        REF_DIR / "module-specs.md",
        REF_DIR / "cognitive-sensors.md",
        REF_DIR / "rollback-policy.md",
        REF_DIR / "cta-playbook.md",
        REF_DIR / "aeh-cta-bridge.md",
        REF_DIR / "mode-selection.md",
    ]
    for path in required_files:
        results.append(
            CheckResult(
                suite="artifact",
                name=f"file-exists:{path.relative_to(ROOT)}",
                passed=path.exists(),
                detail="exists" if path.exists() else "missing",
            )
        )

    readme_sections = [
        "Agent = Model + Writing Harness",
        "The One Spine",
        "The Core Architecture",
        "How The System Runs",
        "Light vs Heavy Use",
        "Repository Knowledge as the System of Record",
        "Harness Design Principles",
    ]
    ok, missing = contains_all(readme, readme_sections)
    results.append(
        CheckResult(
            suite="artifact",
            name="readme-core-sections",
            passed=ok,
            detail="all sections present" if ok else f"missing: {', '.join(missing)}",
        )
    )

    skill_sections = [
        "Harness Framing",
        "Workflow",
        "Knowledge Loading",
        "Success Condition",
        "Set the cognitive baseline",
    ]
    ok, missing = contains_all(skill, skill_sections)
    results.append(
        CheckResult(
            suite="artifact",
            name="skill-core-sections",
            passed=ok,
            detail="all sections present" if ok else f"missing: {', '.join(missing)}",
        )
    )

    ok, missing = contains_all(
        refs.get("rubric.md", ""),
        [
            "Clarity of Purpose",
            "Audience Specificity",
            "Point of View",
            "Specificity and Concreteness",
            "Insight Density",
            "Structural Focus",
            "Voice Credibility",
            "Reader Usefulness",
            "Trustworthiness",
            "Memorability",
        ],
    )
    results.append(
        CheckResult(
            suite="artifact",
            name="rubric-dimensions",
            passed=ok,
            detail="10 dimensions present" if ok else f"missing: {', '.join(missing)}",
        )
    )

    ok, missing = contains_all(
        refs.get("failure-taxonomy.md", ""),
        [
            "generic_abstraction",
            "overexplained",
            "no_real_thesis",
            "false_balance",
            "stock_phrase",
            "weak_example",
            "empty_empathy",
            "uniform_rhythm",
            "insightless_summary",
            "speaker_invisible",
        ],
    )
    results.append(
        CheckResult(
            suite="artifact",
            name="failure-taxonomy-tags",
            passed=ok,
            detail="all failure tags present" if ok else f"missing: {', '.join(missing)}",
        )
    )

    ok, missing = contains_all(
        refs.get("prompt-templates.md", ""),
        [
            "Rewrite for Authored Quality",
            "Evaluate a Draft",
            "Build a Writing Spec",
            "Editorial Pass",
        ],
    )
    results.append(
        CheckResult(
            suite="artifact",
            name="prompt-template-groups",
            passed=ok,
            detail="template groups present" if ok else f"missing: {', '.join(missing)}",
        )
    )

    ok, missing = contains_all(
        "\n".join(
            refs.get(name, "")
            for name in [
                "cognitive-baseline.md",
                "aeh-architecture.md",
                "module-specs.md",
                "cognitive-sensors.md",
                "rollback-policy.md",
                "cta-playbook.md",
                "aeh-cta-bridge.md",
                "mode-selection.md",
            ]
        ),
        [
            "K",
            "P",
            "A",
            "Assert",
            "Exception",
            "Handler",
            "Log",
            "M-01",
            "M-05",
            "Rollback Mapping",
            "critical incident",
            "GOMS",
            "retell bullets",
            "AEH decides the route",
            "Light rewrite",
            "CTA surgery",
        ],
    )
    results.append(
        CheckResult(
            suite="artifact",
            name="cognitive-harness-references",
            passed=ok,
            detail="cognitive references present" if ok else f"missing: {', '.join(missing)}",
        )
    )

    compact_skill = len(skill.splitlines()) <= 250
    results.append(
        CheckResult(
            suite="artifact",
            name="skill-entrypoint-compactness",
            passed=compact_skill,
            detail=f"{len(skill.splitlines())} lines",
        )
    )

    return results


def behavioral_coverage_checks() -> list[CheckResult]:
    results: list[CheckResult] = []
    corpus = "\n".join(
        [
            read(README),
            read(SKILL),
            *(read(path) for path in sorted(REF_DIR.glob("*.md"))),
        ]
    )

    cases = json.loads(read(CASES))
    for case in cases:
        ok, missing = contains_all(corpus, case["required_terms"])
        results.append(
            CheckResult(
                suite="coverage",
                name=case["id"],
                passed=ok,
                detail=case["description"] if ok else f"missing terms: {', '.join(missing)}",
            )
        )

    return results


def summarize(results: list[CheckResult]) -> dict:
    passed = sum(1 for item in results if item.passed)
    total = len(results)
    by_suite: dict[str, dict[str, int]] = {}
    for item in results:
        bucket = by_suite.setdefault(item.suite, {"passed": 0, "total": 0})
        bucket["total"] += 1
        if item.passed:
            bucket["passed"] += 1
    return {
        "passed": passed,
        "total": total,
        "pass_rate": round((passed / total) * 100, 2) if total else 0.0,
        "by_suite": by_suite,
    }


def print_report(results: list[CheckResult]) -> None:
    summary = summarize(results)
    print("Writing Harness Eval Report")
    print(f"Passed {summary['passed']}/{summary['total']} checks ({summary['pass_rate']}%)")
    print()
    for suite, stats in summary["by_suite"].items():
        print(f"[{suite}] {stats['passed']}/{stats['total']} passed")
        for item in [r for r in results if r.suite == suite]:
            status = "PASS" if item.passed else "FAIL"
            print(f"  - {status} {item.name}: {item.detail}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", dest="json_path")
    args = parser.parse_args()

    results = artifact_checks() + behavioral_coverage_checks()
    print_report(results)

    if args.json_path:
        path = Path(args.json_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "summary": summarize(results),
            "results": [asdict(item) for item in results],
        }
        path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        print()
        print(f"Wrote JSON report to {path}")

    return 0 if all(item.passed for item in results) else 1


if __name__ == "__main__":
    sys.exit(main())
