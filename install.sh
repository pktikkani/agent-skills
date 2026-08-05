#!/usr/bin/env bash
# Install the skills in this repo.
#
#   ./install.sh              global: claude/skills -> ~/.claude/skills
#                                     codex/prompts -> ~/.codex/prompts
#   ./install.sh --project    project: claude/skills -> ./.claude/skills
#                                     (Codex prompts are global-only; skipped)
#
# Idempotent: re-running overwrites the installed copies with this repo's version.
# Existing skills with the same name are replaced. Unrelated skills are untouched.

set -euo pipefail

SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MODE="global"

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
  echo "project mode: skipped Codex prompts (Codex reads ~/.codex/prompts only)"
  exit 0
fi

PROMPT_DEST="$HOME/.codex/prompts"
mkdir -p "$PROMPT_DEST"

pcount=0
for file in "$SRC"/codex/prompts/*.md; do
  name="$(basename "$file")"
  cp "$file" "$PROMPT_DEST/$name"
  echo "  prompt ${name%.md} -> $PROMPT_DEST/$name"
  pcount=$((pcount + 1))
done
echo "installed $pcount Codex prompt(s)"
