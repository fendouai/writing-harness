#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
CASES_PATH = ROOT / "evals" / "benchmarks" / "cases.json"


def read_cases() -> list[dict]:
    return json.loads(CASES_PATH.read_text(encoding="utf-8"))


def build_packet(case: dict, output_path: Path) -> str:
    return f"""# Writing Harness Benchmark Packet

Case ID: {case["id"]}
Title: {case["title"]}
Surface: {case["surface"]}
Audience: {case["audience"]}
Task: {case["task"]}

Instructions:
1. Use the Writing Harness skill.
2. Rewrite the draft for authored quality.
3. Preserve the required facts.
4. Avoid the banned phrases.
5. Return only the rewritten text in the output file.

Required facts:
- {chr(10).join(f"- {item}" for item in case["preserve_facts_all"])}

Strengthening signals:
- {chr(10).join(f"- {item}" for item in case["strengthen_with_any"])}

Avoid phrases:
- {chr(10).join(f"- {item}" for item in case["avoid_phrases"])}

Suggested weak patterns to reduce:
- {chr(10).join(f"- {item}" for item in case["reduce_phrases"])}

Write the final rewrite to:
{output_path}

Draft:
{case["input_text"]}
"""


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--outdir", required=True)
    parser.add_argument("--cases", help="Comma-separated case ids")
    args = parser.parse_args()

    cases = read_cases()
    if args.cases:
        wanted = {item.strip() for item in args.cases.split(",") if item.strip()}
        cases = [case for case in cases if case["id"] in wanted]

    outdir = Path(args.outdir)
    packets_dir = outdir / "packets"
    results_dir = outdir / "results"
    packets_dir.mkdir(parents=True, exist_ok=True)
    results_dir.mkdir(parents=True, exist_ok=True)

    manifest: list[dict] = []
    for case in cases:
        result_path = results_dir / f"{case['id']}.md"
        packet = build_packet(case, result_path.resolve())
        packet_path = packets_dir / f"{case['id']}.md"
        packet_path.write_text(packet, encoding="utf-8")
        manifest.append(
            {
                "case_id": case["id"],
                "packet_file": str(packet_path),
                "result_file": str(result_path),
            }
        )

    manifest_path = outdir / "run-manifest.json"
    manifest_path.write_text(json.dumps({"cases": manifest}, indent=2), encoding="utf-8")
    print(f"Wrote benchmark packets to {packets_dir}")
    print(f"Wrote run manifest to {manifest_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
