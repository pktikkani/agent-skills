#!/usr/bin/env python3
"""Per-function CRAP scores for TS/JS: CRAP(m) = CC^2 * (1-cov)^3 + CC.

Inputs: eslint JSON report (complexity rule) + istanbul/c8 coverage-final.json.
  npx eslint <src> -f json --rule '{"complexity":["warn",0]}' > eslint.json
  npx c8 --reporter=json <test cmd>   # writes coverage/coverage-final.json
  python crap_ts.py eslint.json coverage-final.json [--threshold 8]

Prints JSON (worst offenders first); exits 1 if any function >= threshold,
so the loop can gate on the exit code. Exit 2 on usage/input error.
"""
import argparse
import json
import os
import re
import sys

# eslint complexity rule message: "Function 'foo' has a complexity of 7. ..."
COMPLEXITY_RE = re.compile(r"^(.*?) has a complexity of (\d+)")


def parse_eslint(report):
    """[(file, line, name, cc)] from an eslint JSON report."""
    out = []
    for entry in report:
        path = os.path.normpath(entry.get("filePath", ""))
        for msg in entry.get("messages", []):
            if msg.get("ruleId") != "complexity":
                continue
            m = COMPLEXITY_RE.match(msg.get("message", ""))
            if not m:
                continue
            name = m.group(1).strip().strip(".")
            # "Function 'foo'" -> "foo"; "Arrow function" stays as-is
            q = re.search(r"'([^']*)'", name)
            if q:
                name = q.group(1)
            out.append((path, msg.get("line", 0), name, int(m.group(2))))
    return out


def statement_coverage(file_cov, start, end):
    """Fraction of statements whose start line falls in [start, end]."""
    smap = file_cov.get("statementMap", {})
    hits = file_cov.get("s", {})
    covered = total = 0
    for sid, loc in smap.items():
        line = (loc.get("start") or {}).get("line")
        if line is None or not (start <= line <= end):
            continue
        total += 1
        if hits.get(sid, 0) > 0:
            covered += 1
    return covered / total if total else None


def function_coverage(file_cov, line):
    """Coverage for the fnMap entry matching `line`; None if no match.

    eslint anchors multiline arrow functions at the `=>` token while istanbul
    anchors the declaration, so exact/nearest-line matching alone misreads
    covered functions as uncovered. Prefer the smallest fnMap loc range that
    CONTAINS the line; fall back to nearest decl within 1 line."""
    fmap = file_cov.get("fnMap", {})
    hits = file_cov.get("f", {})
    best_id = best_delta = None
    enclosing_id = enclosing_span = None
    for fid, fn in fmap.items():
        decl = (fn.get("decl") or fn.get("loc") or {}).get("start", {})
        fline = decl.get("line")
        if fline is None:
            continue
        delta = abs(fline - line)
        if best_delta is None or delta < best_delta:
            best_id, best_delta = fid, delta
        loc = fn.get("loc") or {}
        start = (loc.get("start") or {}).get("line")
        end = (loc.get("end") or {}).get("line")
        if start is not None and end is not None and start <= line <= end:
            span = end - start
            if enclosing_span is None or span < enclosing_span:
                enclosing_id, enclosing_span = fid, span
    if best_id is None or best_delta > 1:
        best_id = enclosing_id
    if best_id is None:
        return None
    fn = fmap[best_id]
    loc = fn.get("loc") or {}
    start = (loc.get("start") or {}).get("line")
    end = (loc.get("end") or {}).get("line")
    if start is not None and end is not None:
        cov = statement_coverage(file_cov, start, end)
        if cov is not None:
            return cov
    # no statements attributed: fall back to the function hit count
    return 1.0 if hits.get(best_id, 0) > 0 else 0.0


def match_file(cov_files, path):
    """Coverage entry for `path`, tolerating absolute vs relative path forms."""
    if path in cov_files:
        return cov_files[path]
    for key, val in cov_files.items():
        if key.endswith(os.sep + path) or path.endswith(os.sep + key):
            return val
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("eslint_json")
    ap.add_argument("coverage_json")
    ap.add_argument("--threshold", type=float, default=8.0)
    ap.add_argument("--top", type=int, default=20)
    args = ap.parse_args()

    try:
        with open(args.eslint_json) as f:
            eslint = json.load(f)
        with open(args.coverage_json) as f:
            coverage = json.load(f)
    except (OSError, ValueError) as e:
        print("error: %s" % e, file=sys.stderr)
        sys.exit(2)

    if not isinstance(eslint, list) or not isinstance(coverage, dict):
        print("error: expected eslint JSON array + istanbul coverage object",
              file=sys.stderr)
        sys.exit(2)

    cov_files = {os.path.normpath(k): v for k, v in coverage.items()}

    rows = []
    for path, line, name, cc in parse_eslint(eslint):
        file_cov = match_file(cov_files, path)
        cov = function_coverage(file_cov, line) if file_cov else None
        # missing from coverage = uncovered (conservative reading)
        cov = 0.0 if cov is None else cov
        crap = cc * cc * (1 - cov) ** 3 + cc
        rows.append({
            "file": path,
            "function": name,
            "line": line,
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
