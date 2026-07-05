#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
from pathlib import Path

from writing_checks import build_default_cw_artifact, build_default_trace_template


ROOT = Path(__file__).resolve().parent.parent
CASES_PATH = ROOT / "evals" / "benchmarks" / "cases.json"


def read_cases() -> list[dict]:
    return json.loads(CASES_PATH.read_text(encoding="utf-8"))


def bullets(items: list[str]) -> str:
    return "\n".join(f"- {item}" for item in items)


def contract_bullets(contracts: list[dict]) -> str:
    return "\n".join(f"- {item['name']}: match {', '.join(item['terms'])}" for item in contracts)


def build_packet(case: dict, output_path: Path, trace_path: Path, cw_path: Path) -> str:
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
5. Satisfy the genre contracts.
6. Write the final rewrite to the output file.
7. Write a full CW artifact sidecar.
8. Make sure the CW artifact contains a trace showing spec -> diagnose -> rewrite -> evaluate.

Required facts:
{bullets(case["preserve_facts_all"])}

Strengthening signals:
{bullets(case["strengthen_with_any"])}

Avoid phrases:
{bullets(case["avoid_phrases"])}

Suggested weak patterns to reduce:
{bullets(case["reduce_phrases"])}

Genre contracts:
{contract_bullets(case.get("genre_contracts", []))}

Write the final rewrite to:
{output_path}

Write the trace JSON to:
{trace_path}

Trace JSON must contain:
- spec
- diagnose
- rewrite
- evaluate

Write the CW artifact JSON to:
{cw_path}

CW artifact must contain:
- baseline
- architecture
- modules
- trace
- unit_tests
- integration
- rollback

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
        trace_path = results_dir / f"{case['id']}.trace.json"
        cw_path = results_dir / f"{case['id']}.cw.json"
        packet = build_packet(case, result_path.resolve(), trace_path.resolve(), cw_path.resolve())
        packet_path = packets_dir / f"{case['id']}.md"
        packet_path.write_text(packet, encoding="utf-8")
        trace_path.write_text(json.dumps(build_default_trace_template(case), indent=2), encoding="utf-8")
        cw_path.write_text(json.dumps(build_default_cw_artifact(case), indent=2), encoding="utf-8")
        manifest.append(
            {
                "case_id": case["id"],
                "packet_file": str(packet_path),
                "result_file": str(result_path),
                "trace_file": str(trace_path),
                "cw_file": str(cw_path),
            }
        )

    manifest_path = outdir / "run-manifest.json"
    manifest_path.write_text(json.dumps({"cases": manifest}, indent=2), encoding="utf-8")
    print(f"Wrote benchmark packets to {packets_dir}")
    print(f"Wrote run manifest to {manifest_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
