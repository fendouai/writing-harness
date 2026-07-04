#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", required=True)
    args = parser.parse_args()

    manifest_path = Path(args.manifest)
    data = json.loads(manifest_path.read_text(encoding="utf-8"))
    cases = data.get("cases", [])

    completed = 0
    for case in cases:
        result_file = Path(case["result_file"])
        exists = result_file.exists() and result_file.read_text(encoding="utf-8").strip() != ""
        if exists:
            completed += 1
        print(f"{'DONE' if exists else 'PENDING'} {case['case_id']} -> {result_file}")

    total = len(cases)
    print(f"Completed {completed}/{total}")
    return 0 if completed == total else 1


if __name__ == "__main__":
    raise SystemExit(main())
