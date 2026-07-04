#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
CASES_PATH = ROOT / "evals" / "benchmarks" / "cases.json"


def read_cases() -> list[dict]:
    return json.loads(CASES_PATH.read_text(encoding="utf-8"))


def build_packet(case: dict, left_text: str, right_text: str, output_path: Path) -> str:
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

Preserve facts:
- {chr(10).join(f"- {item}" for item in case["preserve_facts_all"])}

Avoid phrases:
- {chr(10).join(f"- {item}" for item in case["avoid_phrases"])}

LEFT candidate:
{left_text}

RIGHT candidate:
{right_text}

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
        result_path = results_dir / f"{case['id']}.json"
        packet = build_packet(case, left_text, right_text, result_path.resolve())
        packet_path = packets_dir / f"{case['id']}.md"
        packet_path.write_text(packet, encoding="utf-8")
        manifest.append(
            {
                "case_id": case["id"],
                "packet_file": str(packet_path),
                "result_file": str(result_path),
            }
        )

    manifest_path = outdir / "judge-manifest.json"
    manifest_path.write_text(json.dumps({"cases": manifest}, indent=2), encoding="utf-8")
    print(f"Wrote judge packets to {packets_dir}")
    print(f"Wrote judge manifest to {manifest_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
