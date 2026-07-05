#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
from pathlib import Path


REQUIRED_KEYS = [
    "winner",
    "left_score",
    "right_score",
    "confidence",
    "summary",
    "strengths_left",
    "strengths_right",
    "risks_left",
    "risks_right",
]

TRACE_KEYS = [
    "trace_winner",
    "trace_notes_left",
    "trace_notes_right",
]

COGNITIVE_KEYS = [
    "cognitive_winner",
    "cognitive_notes_left",
    "cognitive_notes_right",
]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--results-dir", required=True)
    parser.add_argument("--json")
    args = parser.parse_args()

    results_dir = Path(args.results_dir)
    results = []
    wins = {"left": 0, "right": 0, "tie": 0}
    trace_wins = {"left": 0, "right": 0, "tie": 0}
    cognitive_wins = {"left": 0, "right": 0, "tie": 0}
    qa = {"missing_required_keys": 0, "missing_trace_keys": 0, "missing_cognitive_keys": 0}

    for path in sorted(results_dir.glob("*.json")):
        payload = json.loads(path.read_text(encoding="utf-8"))
        payload["file"] = str(path)
        missing_required = [key for key in REQUIRED_KEYS if key not in payload]
        missing_trace = [key for key in TRACE_KEYS if key not in payload]
        missing_cognitive = [key for key in COGNITIVE_KEYS if key not in payload]
        payload["qa"] = {
            "missing_required_keys": missing_required,
            "missing_trace_keys": missing_trace,
            "missing_cognitive_keys": missing_cognitive,
            "trace_aware": not missing_trace,
            "cognitive_aware": not missing_cognitive,
        }
        if missing_required:
            qa["missing_required_keys"] += 1
        if missing_trace:
            qa["missing_trace_keys"] += 1
        if missing_cognitive:
            qa["missing_cognitive_keys"] += 1
        results.append(payload)
        winner = payload.get("winner", "tie")
        wins[winner] = wins.get(winner, 0) + 1
        trace_winner = payload.get("trace_winner", "tie")
        trace_wins[trace_winner] = trace_wins.get(trace_winner, 0) + 1
        cognitive_winner = payload.get("cognitive_winner", "tie")
        cognitive_wins[cognitive_winner] = cognitive_wins.get(cognitive_winner, 0) + 1

    summary = {
        "total_cases": len(results),
        "wins": wins,
        "trace_wins": trace_wins,
        "cognitive_wins": cognitive_wins,
        "qa": qa,
        "results": results,
    }

    print(json.dumps(summary, indent=2))

    if args.json:
        out_path = Path(args.json)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
        print(f"Wrote JSON report to {out_path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
