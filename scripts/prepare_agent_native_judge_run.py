#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
from pathlib import Path

from writing_checks import (
    cw_artifact_path_for_candidate,
    load_cw_artifact_if_present,
    load_trace_if_present,
    trace_path_for_candidate,
)


ROOT = Path(__file__).resolve().parent.parent
CASES_PATH = ROOT / "evals" / "benchmarks" / "cases.json"


def read_cases() -> list[dict]:
    return json.loads(CASES_PATH.read_text(encoding="utf-8"))


def bullets(items: list[str]) -> str:
    return "\n".join(f"- {item}" for item in items)


def contract_bullets(contracts: list[dict]) -> str:
    return "\n".join(f"- {item['name']}" for item in contracts)


def build_packet(
    case: dict,
    left_text: str,
    right_text: str,
    left_trace: dict | None,
    right_trace: dict | None,
    left_cw: dict | None,
    right_cw: dict | None,
    left_trace_path: Path,
    right_trace_path: Path,
    left_cw_path: Path,
    right_cw_path: Path,
    output_path: Path,
) -> str:
    return f"""# Writing Harness Judge Packet

Case ID: {case["id"]}
Title: {case["title"]}
Surface: {case["surface"]}
Audience: {case["audience"]}
Task: {case["task"]}

Judge standard:
- authored quality over surface human-likeness
- stronger specificity
- stronger judgment
- better audience fit
- more useful language
- fewer generic, padded, or stock phrases
- better harness discipline through spec -> diagnose -> rewrite -> evaluate
- stronger baseline, module, and rollback discipline

Preserve facts:
{bullets(case["preserve_facts_all"])}

Avoid phrases:
{bullets(case["avoid_phrases"])}

Genre contracts:
{contract_bullets(case.get("genre_contracts", []))}

LEFT candidate:
{left_text}

LEFT trace file:
{left_trace_path}

LEFT trace payload:
{json.dumps(left_trace, indent=2) if left_trace is not None else "MISSING"}

LEFT CW artifact file:
{left_cw_path}

LEFT CW artifact payload:
{json.dumps(left_cw, indent=2) if left_cw is not None else "MISSING"}

RIGHT candidate:
{right_text}

RIGHT trace file:
{right_trace_path}

RIGHT trace payload:
{json.dumps(right_trace, indent=2) if right_trace is not None else "MISSING"}

RIGHT CW artifact file:
{right_cw_path}

RIGHT CW artifact payload:
{json.dumps(right_cw, indent=2) if right_cw is not None else "MISSING"}

Write valid JSON to:
{output_path}

Required JSON keys:
- winner: "left" | "right" | "tie"
- left_score: integer 0-100
- right_score: integer 0-100
- confidence: integer 1-5
- summary: short string
- strengths_left: array of strings
- strengths_right: array of strings
- risks_left: array of strings
- risks_right: array of strings
- trace_winner: "left" | "right" | "tie"
- trace_notes_left: array of strings
- trace_notes_right: array of strings
- cognitive_winner: "left" | "right" | "tie"
- cognitive_notes_left: array of strings
- cognitive_notes_right: array of strings
"""


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--left-dir", required=True)
    parser.add_argument("--right-dir", required=True)
    parser.add_argument("--outdir", required=True)
    args = parser.parse_args()

    left_dir = Path(args.left_dir)
    right_dir = Path(args.right_dir)
    outdir = Path(args.outdir)
    packets_dir = outdir / "packets"
    results_dir = outdir / "results"
    packets_dir.mkdir(parents=True, exist_ok=True)
    results_dir.mkdir(parents=True, exist_ok=True)

    manifest: list[dict] = []
    for case in read_cases():
        left_path = left_dir / f"{case['id']}.md"
        right_path = right_dir / f"{case['id']}.md"
        left_text = left_path.read_text(encoding="utf-8")
        right_text = right_path.read_text(encoding="utf-8")
        left_trace = load_trace_if_present(left_path)
        right_trace = load_trace_if_present(right_path)
        left_cw = load_cw_artifact_if_present(left_path)
        right_cw = load_cw_artifact_if_present(right_path)
        left_trace_path = trace_path_for_candidate(left_path)
        right_trace_path = trace_path_for_candidate(right_path)
        left_cw_path = cw_artifact_path_for_candidate(left_path)
        right_cw_path = cw_artifact_path_for_candidate(right_path)
        result_path = results_dir / f"{case['id']}.json"
        packet = build_packet(
            case,
            left_text,
            right_text,
            left_trace,
            right_trace,
            left_cw,
            right_cw,
            left_trace_path.resolve(),
            right_trace_path.resolve(),
            left_cw_path.resolve(),
            right_cw_path.resolve(),
            result_path.resolve(),
        )
        packet_path = packets_dir / f"{case['id']}.md"
        packet_path.write_text(packet, encoding="utf-8")
        manifest.append(
            {
                "case_id": case["id"],
                "packet_file": str(packet_path),
                "result_file": str(result_path),
                "left_trace_file": str(left_trace_path),
                "right_trace_file": str(right_trace_path),
                "left_cw_file": str(left_cw_path),
                "right_cw_file": str(right_cw_path),
            }
        )

    manifest_path = outdir / "judge-manifest.json"
    manifest_path.write_text(json.dumps({"cases": manifest}, indent=2), encoding="utf-8")
    print(f"Wrote judge packets to {packets_dir}")
    print(f"Wrote judge manifest to {manifest_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
