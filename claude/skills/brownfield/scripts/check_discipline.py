#!/usr/bin/env python3
"""Portable, zero-dependency discipline gate for a brownfield (existing) project.

Why this exists: a lean architecture contract (BLUEPRINT.md) is worthless if nothing
enforces it. This gate is the un-ignorable check that a source file has not become a
god-file and that every module explains itself. It uses only the Python stdlib so it
runs anywhere with no install step, and it is wired as a pre-commit hook + `make check`
(or a `"check"` npm script) by the /brownfield skill.

Brownfield difference — the RATCHET: an existing repo already has files over the limit.
Instead of failing forever or blessing the mess, BLUEPRINT.md declares per-file
"grandfathered" caps for the genuinely-largest files. Each grandfathered file is checked
against its OWN cap (today's size) — it may not GROW, and should shrink. Every other file
is held to the standard limits. New god-files are still blocked.

Checks, per source file under SRC_DIRS:
  1. File LOC <= its cap  (grandfathered cap if listed, else the global file limit)
  2. Every function LOC <= fn limit (default 50; override in BLUEPRINT.md; Python only)
  3. A module-level docstring is present (WHY the module exists; Python only)

Config read from BLUEPRINT.md if present:
  - Global limits: a line containing "400 lines/file" and "50 lines/function".
  - Grandfathered caps: a block beginning with a line containing "Grandfathered caps",
    followed by lines each naming a path and a number, e.g.
        `src/legacy/parser.py` capped at 1180 lines
    Each such file is checked against that number instead of the global file limit.

Usage:  python scripts/check_discipline.py [--file-limit 400] [--fn-limit 50]
Exit 0 = clean, 1 = violations. Debug from the printed list, do not guess.
"""

from __future__ import annotations

import argparse
import ast
import re
import sys
from pathlib import Path

FILE_LIMIT_DEFAULT = 400
FN_LIMIT_DEFAULT = 50

REPO_ROOT = Path(__file__).resolve().parent.parent
# Directories that hold first-party source. Extend per project if needed.
SRC_DIRS = ["src", "app", "lib"]
PY_EXCLUDE_DIRS = {"__pycache__", ".venv", "venv", "node_modules", ".git", "dist", "build"}
CODE_SUFFIXES = {".py", ".js", ".jsx", ".ts", ".tsx", ".go", ".rs", ".rb"}


def read_limits_from_blueprint() -> tuple[int, int]:
    """Parse global hard limits out of BLUEPRINT.md so the gate and doc never drift."""
    bp = REPO_ROOT / "BLUEPRINT.md"
    file_limit, fn_limit = FILE_LIMIT_DEFAULT, FN_LIMIT_DEFAULT
    if not bp.exists():
        return file_limit, fn_limit
    text = bp.read_text(encoding="utf-8", errors="ignore")
    m_file = re.search(r"(\d+)\s*lines?\s*/\s*file", text, re.IGNORECASE)
    m_fn = re.search(r"(\d+)\s*lines?\s*/\s*function", text, re.IGNORECASE)
    if m_file:
        file_limit = int(m_file.group(1))
    if m_fn:
        fn_limit = int(m_fn.group(1))
    return file_limit, fn_limit


def read_grandfathered_caps() -> dict[str, int]:
    """Parse per-file grandfathered caps from BLUEPRINT.md.

    A cap declaration is any line naming a source path AND the word "capped" AND a line
    count, e.g.:  `src/legacy/parser.py` capped at 1180 lines.
    Returns {posix_relpath: cap}. Matching is line-level and order-independent, so a prose
    mention of "grandfathered caps" elsewhere in the doc will not confuse it — only lines
    with the canonical "<path> ... capped at <n> lines" shape are treated as declarations.
    The ratchet: these files are held to today's size, not the global limit — they may not grow.
    """
    bp = REPO_ROOT / "BLUEPRINT.md"
    caps: dict[str, int] = {}
    if not bp.exists():
        return caps
    # Path in backticks OR a bare path like a/b.ext, then "capped ... <n> lines" on the same line.
    pat = re.compile(
        r"(?:`([^`]+)`|([\w./\-]+\.[\w]+))[^\n]*?\bcapped\b[^\n]*?(\d+)\s*lines?",
        re.IGNORECASE,
    )
    for raw in bp.read_text(encoding="utf-8", errors="ignore").splitlines():
        m = pat.search(raw)
        if m:
            path = (m.group(1) or m.group(2)).strip()
            caps[Path(path).as_posix()] = int(m.group(3))
    return caps


def iter_source_files() -> list[Path]:
    """Collect first-party source files, skipping vendored/generated trees."""
    files: list[Path] = []
    for src in SRC_DIRS:
        root = REPO_ROOT / src
        if not root.exists():
            continue
        for path in root.rglob("*"):
            if path.is_dir():
                continue
            if any(part in PY_EXCLUDE_DIRS for part in path.parts):
                continue
            if path.suffix in CODE_SUFFIXES:
                files.append(path)
    return sorted(files)


def check_file_loc(path: Path, limit: int, caps: dict[str, int]) -> list[str]:
    rel = path.relative_to(REPO_ROOT).as_posix()
    effective = caps.get(rel, limit)
    grandfathered = rel in caps
    loc = sum(1 for _ in path.open("r", encoding="utf-8", errors="ignore"))
    if loc > effective:
        if grandfathered:
            return [
                f"  {rel}: {loc} lines > grandfathered cap {effective} "
                "(this file may NOT grow — shrink it)"
            ]
        return [f"  {rel}: {loc} lines > file limit {effective} (god-file forming — split it)"]
    return []


def check_python(path: Path, fn_limit: int) -> list[str]:
    """Function-length and module-docstring checks. Python-only (uses ast)."""
    rel = path.relative_to(REPO_ROOT).as_posix()
    problems: list[str] = []
    try:
        tree = ast.parse(path.read_text(encoding="utf-8", errors="ignore"))
    except SyntaxError as exc:
        return [f"  {rel}: does not parse ({exc.msg} at line {exc.lineno})"]

    if ast.get_docstring(tree) is None:
        problems.append(f"  {rel}: missing module docstring (say WHY this module exists)")

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            end = getattr(node, "end_lineno", node.lineno)
            span = end - node.lineno + 1
            if span > fn_limit:
                problems.append(
                    f"  {rel}:{node.lineno} function `{node.name}` is {span} lines "
                    f"> function limit {fn_limit} (decompose it)"
                )
    return problems


def main() -> int:
    bp_file, bp_fn = read_limits_from_blueprint()
    caps = read_grandfathered_caps()
    ap = argparse.ArgumentParser(description="Zero-dependency project discipline gate.")
    ap.add_argument("--file-limit", type=int, default=bp_file)
    ap.add_argument("--fn-limit", type=int, default=bp_fn)
    ap.add_argument(
        "--loc-only",
        action="store_true",
        help=(
            "Enforce only the file-LOC ratchet; skip the Python function-length and "
            "module-docstring checks. Use on a brownfield repo whose legacy functions/"
            "docstrings would otherwise block every commit — the god-file freeze still "
            "holds, and function/docstring debt is tracked in REVIEW_LEDGER.md instead."
        ),
    )
    args = ap.parse_args()

    files = iter_source_files()
    if not files:
        print(f"No source files found under {SRC_DIRS}; nothing to check.")
        return 0

    failures: list[str] = []
    for path in files:
        failures += check_file_loc(path, args.file_limit, caps)
        if path.suffix == ".py" and not args.loc_only:
            failures += check_python(path, args.fn_limit)

    if failures:
        print("\n[FAIL] Discipline gate failed:", file=sys.stderr)
        print("\n".join(failures), file=sys.stderr)
        print(
            f"\nLimits: {args.file_limit} lines/file, {args.fn_limit} lines/function "
            f"(set in BLUEPRINT.md; {len(caps)} grandfathered file(s) held to their own cap). "
            "Split god-files, add missing docstrings, shrink grandfathered files — never grow them.",
            file=sys.stderr,
        )
        return 1

    print(
        f"[OK] Discipline gate passed: {len(files)} source files within "
        f"{args.file_limit} lines/file, {args.fn_limit} lines/function "
        f"({len(caps)} grandfathered)."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
