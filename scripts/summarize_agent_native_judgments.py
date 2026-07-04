#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--results-dir", required=True)
    parser.add_argument("--json")
    args = parser.parse_args()

    results_dir = Path(args.results_dir)
    results = []
    wins = {"left": 0, "right": 0, "tie": 0}

    for path in sorted(results_dir.glob("*.json")):
        payload = json.loads(path.read_text(encoding="utf-8"))
        payload["file"] = str(path)
        results.append(payload)
        winner = payload.get("winner", "tie")
        wins[winner] = wins.get(winner, 0) + 1

    summary = {
        "total_cases": len(results),
        "wins": wins,
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
