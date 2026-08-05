#!/usr/bin/env python3
"""Per-function CRAP scores for Python: CRAP(m) = CC^2 * (1-cov)^3 + CC.

Inputs: radon cyclomatic-complexity JSON + coverage.py JSON.
  radon cc -j <src> > radon.json
  coverage run -m pytest && coverage json -o coverage.json
  python crap_py.py radon.json coverage.json [--threshold 8]

Prints JSON (worst offenders first); exits 1 if any function >= threshold,
so the loop can gate on the exit code.
"""
import argparse
import json
import os
import sys


def function_coverage(block, file_cov):
    lines = set(range(block["lineno"], block.get("endline", block["lineno"]) + 1))
    executed = lines & set(file_cov["executed_lines"])
    missing = lines & set(file_cov["missing_lines"])
    total = len(executed) + len(missing)
    # total == 0 means no executable lines attributed; treat as uncovered
    return len(executed) / total if total else 0.0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("radon_json")
    ap.add_argument("coverage_json")
    ap.add_argument("--threshold", type=float, default=8.0)
    ap.add_argument("--top", type=int, default=20)
    args = ap.parse_args()

    with open(args.radon_json) as f:
        radon = json.load(f)
    with open(args.coverage_json) as f:
        cov_files = {os.path.normpath(k): v
                     for k, v in json.load(f)["files"].items()}

    rows = []
    for path, blocks in radon.items():
        if not isinstance(blocks, list):  # radon reports errors as dicts
            continue
        key = os.path.normpath(path)
        file_cov = cov_files.get(key)
        for b in blocks:
            cc = b["complexity"]
            cov = function_coverage(b, file_cov) if file_cov else 0.0
            crap = cc * cc * (1 - cov) ** 3 + cc
            rows.append({
                "file": key,
                "function": b["name"],
                "line": b["lineno"],
                "cc": cc,
                "coverage": round(cov, 2),
                "crap": round(crap, 1),
            })

    rows.sort(key=lambda r: -r["crap"])
    over = [r for r in rows if r["crap"] >= args.threshold]
    print(json.dumps({
        "threshold": args.threshold,
        "functions_scored": len(rows),
        "over_threshold": len(over),
        "worst": rows[:args.top],
    }, indent=2))
    sys.exit(1 if over else 0)


if __name__ == "__main__":
    main()
