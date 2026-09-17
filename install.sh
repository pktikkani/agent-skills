#!/usr/bin/env bash
# Install the skills in this repo.
#
#   ./install.sh              global: claude/skills -> ~/.claude/skills
#                                     five of them  -> ~/.codex/skills
#   ./install.sh --project    project: claude/skills -> ./.claude/skills
#                                     (Codex skipped)
#
# Idempotent: re-running overwrites the installed copies with this repo's version.
# Existing skills with the same name are replaced. Unrelated skills are untouched.

set -euo pipefail

SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MODE="global"
CODEX_SKILLS="greenfield brownfield handoff eval-discipline crap-score"

for arg in "$@"; do
  case "$arg" in
    --project) MODE="project" ;;
    -h|--help) sed -n '2,11p' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
    *) echo "unknown option: $arg (try --help)" >&2; exit 2 ;;
  esac
done

if [ "$MODE" = "project" ]; then
  SKILL_DEST="$PWD/.claude/skills"
else
  SKILL_DEST="$HOME/.claude/skills"
fi

mkdir -p "$SKILL_DEST"

count=0
for dir in "$SRC"/claude/skills/*/; do
  name="$(basename "$dir")"
  rm -rf "$SKILL_DEST/$name"
  cp -R "$dir" "$SKILL_DEST/$name"
  echo "  skill  $name -> $SKILL_DEST/$name"
  count=$((count + 1))
done
echo "installed $count Claude Code skill(s)"

if [ "$MODE" = "project" ]; then
  echo "project mode: skipped Codex"
  exit 0
fi

# Codex CLI reads the same SKILL.md format from ~/.codex/skills (custom prompts are gone).
CODEX_DEST="$HOME/.codex/skills"
mkdir -p "$CODEX_DEST"

ccount=0
for name in $CODEX_SKILLS; do
  rm -rf "$CODEX_DEST/$name"
  cp -R "$SRC/claude/skills/$name" "$CODEX_DEST/$name"
  echo "  codex  $name -> $CODEX_DEST/$name"
  ccount=$((ccount + 1))
done
echo "installed $ccount Codex skill(s)"
