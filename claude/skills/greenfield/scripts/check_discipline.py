#!/usr/bin/env python3
"""Portable, zero-dependency discipline gate for a greenfield project.

Why this exists: a lean architecture contract (BLUEPRINT.md) is worthless if nothing
enforces it. This gate is the un-ignorable check that a source file has not become a
god-file and that every module explains itself. It uses only the Python stdlib so it
runs anywhere with no install step, and it is wired as a pre-commit hook + `make check`
by the /greenfield skill.

Checks, per source file under SRC_DIRS:
  1. File LOC <= file limit         (default 400; override in BLUEPRINT.md)
  2. Every function LOC <= fn limit (default 50;  override in BLUEPRINT.md; Python only)
  3. A module-level docstring is present (WHY the module exists; Python only)

Limits are read from BLUEPRINT.md if it declares them, e.g. a line containing
"400 lines/file" and "50 lines/function"; otherwise the defaults below apply.

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
    """Parse hard limits out of BLUEPRINT.md so the gate and the doc never drift."""
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


def check_file_loc(path: Path, limit: int) -> list[str]:
    loc = sum(1 for _ in path.open("r", encoding="utf-8", errors="ignore"))
    if loc > limit:
        rel = path.relative_to(REPO_ROOT).as_posix()
        return [f"  {rel}: {loc} lines > file limit {limit} (god-file forming — split it)"]
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
    ap = argparse.ArgumentParser(description="Zero-dependency project discipline gate.")
    ap.add_argument("--file-limit", type=int, default=bp_file)
    ap.add_argument("--fn-limit", type=int, default=bp_fn)
    args = ap.parse_args()

    files = iter_source_files()
    if not files:
        print(f"No source files found under {SRC_DIRS}; nothing to check.")
        return 0

    failures: list[str] = []
    for path in files:
        failures += check_file_loc(path, args.file_limit)
        if path.suffix == ".py":
            failures += check_python(path, args.fn_limit)

    if failures:
        print("\n[FAIL] Discipline gate failed:", file=sys.stderr)
        print("\n".join(failures), file=sys.stderr)
        print(
            f"\nLimits: {args.file_limit} lines/file, {args.fn_limit} lines/function "
            "(set in BLUEPRINT.md). Split god-files, add the missing docstrings, "
            "then re-run.",
            file=sys.stderr,
        )
        return 1

    print(
        f"[OK] Discipline gate passed: {len(files)} source files "
        f"within {args.file_limit} lines/file, {args.fn_limit} lines/function."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
