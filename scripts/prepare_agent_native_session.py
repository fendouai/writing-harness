#!/usr/bin/env python3

from __future__ import annotations

import argparse
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
BENCH_SCRIPT = ROOT / "scripts" / "prepare_agent_native_benchmark_run.py"
JUDGE_SCRIPT = ROOT / "scripts" / "prepare_agent_native_judge_run.py"


def run(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True, cwd=ROOT)


def build_benchmark_runbook(session_dir: Path) -> str:
    return f"""# Agent-Native Benchmark Session Runbook

Use this runbook in a single agent session.

## Goal

Process every benchmark packet with the Writing Harness skill and write one final rewrite per case.

## Session Files

- Manifest: {session_dir / "run-manifest.json"}
- Packets directory: {session_dir / "packets"}
- Results directory: {session_dir / "results"}

## Instructions For The Agent

1. Use the Writing Harness skill.
2. Read the manifest first.
3. Process every packet in the packets directory.
4. For each packet:
   - read the case instructions
   - produce one final rewrite
   - write the final text to the requested result file
5. Do not skip cases.
6. Do not write commentary into the result files.
7. After finishing all cases, stop and report completion.

## Suggested user message

Use the Writing Harness skill and complete the benchmark session described in:
{session_dir / "RUNBOOK.md"}

Make sure every packet in {session_dir / "packets"} is processed and every output is written into {session_dir / "results"}.
"""


def build_judge_runbook(session_dir: Path) -> str:
    return f"""# Agent-Native Judge Session Runbook

Use this runbook in a single agent session.

## Goal

Process every judge packet and write one valid JSON judgment per case.

## Session Files

- Manifest: {session_dir / "judge-manifest.json"}
- Packets directory: {session_dir / "packets"}
- Results directory: {session_dir / "results"}

## Instructions For The Agent

1. Read the manifest first.
2. Process every packet in the packets directory.
3. For each packet:
   - compare LEFT vs RIGHT
   - produce valid JSON with the required keys
   - write the JSON to the requested result file
4. Do not skip cases.
5. Do not write prose outside the JSON result files.
6. After finishing all cases, stop and report completion.

## Suggested user message

Complete the pairwise Writing Harness judge session described in:
{session_dir / "RUNBOOK.md"}

Make sure every packet in {session_dir / "packets"} is processed and every JSON result is written into {session_dir / "results"}.
"""


def main() -> int:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="mode", required=True)

    bench = subparsers.add_parser("benchmark")
    bench.add_argument("--outdir", required=True)
    bench.add_argument("--cases")

    judge = subparsers.add_parser("judge")
    judge.add_argument("--left-dir", required=True)
    judge.add_argument("--right-dir", required=True)
    judge.add_argument("--outdir", required=True)

    args = parser.parse_args()

    if args.mode == "benchmark":
        cmd = ["python3", str(BENCH_SCRIPT), "--outdir", args.outdir]
        if args.cases:
            cmd.extend(["--cases", args.cases])
        run(cmd)
        session_dir = Path(args.outdir).resolve()
        runbook = build_benchmark_runbook(session_dir)
    else:
        cmd = [
            "python3",
            str(JUDGE_SCRIPT),
            "--left-dir",
            args.left_dir,
            "--right-dir",
            args.right_dir,
            "--outdir",
            args.outdir,
        ]
        run(cmd)
        session_dir = Path(args.outdir).resolve()
        runbook = build_judge_runbook(session_dir)

    runbook_path = session_dir / "RUNBOOK.md"
    runbook_path.write_text(runbook, encoding="utf-8")
    print(f"Wrote session runbook to {runbook_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
