# handoff — compact this session into STATUS.md

Write (or fully overwrite) `STATUS.md` at the current project root — create it if absent.
It is a SNAPSHOT, not a log: full overwrite every time, never append.
Target ≤120 lines / ~1-2k tokens.

## Template (fixed sections, in this order)

```
# STATUS — <project> — <YYYY-MM-DD>

## Now
What's in flight; the exact next 1-3 actions, with file paths.

## State
What works, what's broken, test status.

## Decisions this session
Only NEW decisions, each with a one-line why. Durable ones should graduate to
BLUEPRINT.md/ADRs — note explicitly when one should.

## Gotchas
Non-obvious traps discovered this session: env quirks, flaky commands, things
that look wrong but are right.

## Pointers
Key files:lines, running processes, external state (open PRs, pending tokens, ...).
```

## Rules

- Concrete over narrative: paths, commands, numbers — no prose recap of the conversation.
- Nothing secret: no tokens/keys — reference their location instead (e.g. "creds in .env").
- If the repo is git-tracked, commit STATUS.md alone with message `handoff: <YYYY-MM-DD>`
  ONLY if the user confirms.
- Re-entry cost must stay under ~2k tokens. If the draft exceeds it, cut State/Decisions
  detail first — never Now/Gotchas.
- Do not duplicate content already captured in other artifacts (BLUEPRINT.md, ADRs, PRDs,
  issues, commits, diffs) — reference them by path in Pointers.
- If arguments were passed, treat them as what the next session will focus on and weight
  Now accordingly.

## Finish

Tell the user the file path and that the next session picks it up via the CLAUDE.md
session-start rule.
