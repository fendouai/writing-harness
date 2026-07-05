#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from writing_checks import lint_writing, summarize_lint, validate_cw_artifact


def lint_path(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    summary = summarize_lint(lint_writing(text))
    summary["file"] = str(path)
    return summary


def lint_cw_path(path: Path) -> dict:
    payload = json.loads(path.read_text(encoding="utf-8"))
    checks = validate_cw_artifact(payload)
    failed = [check for check in checks if not check.passed]
    error_count = sum(1 for check in failed if check.severity == "error")
    result = {
        "file": str(path),
        "passed": error_count == 0,
        "score": max(0, 100 - (error_count * 15) - ((len(failed) - error_count) * 5)),
        "failed_checks": [check.name for check in failed],
        "checks": [check.__dict__ for check in checks],
    }
    return result


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--path")
    parser.add_argument("--dir")
    parser.add_argument("--cw-json")
    parser.add_argument("--json")
    args = parser.parse_args()

    chosen = [value for value in [args.path, args.dir, args.cw_json] if value]
    if not chosen:
        parser.error("Choose --path, --dir, or --cw-json")

    if len(chosen) > 1:
        parser.error("Use only one of --path, --dir, or --cw-json")

    if args.path:
        results = [lint_path(Path(args.path))]
    elif args.cw_json:
        cw_path = Path(args.cw_json)
        if cw_path.exists() and cw_path.is_dir():
            results = [lint_cw_path(path) for path in sorted(cw_path.glob("*.cw.json"))]
        else:
            results = [lint_cw_path(cw_path)]
    else:
        results = [lint_path(path) for path in sorted(Path(args.dir).glob("*.md"))]

    payload = {
        "passed": all(result["passed"] for result in results),
        "results": results,
    }

    print(json.dumps(payload, indent=2))

    if args.json:
        write_json(Path(args.json), payload)
        print(f"Wrote JSON report to {args.json}")

    return 0 if payload["passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
