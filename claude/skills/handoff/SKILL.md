---
name: handoff
description: Compact the current session into the project's STATUS.md re-entry snapshot and append the session's daybook entry. Use when the user types /handoff or says 'hand off' / 'write the handoff'.
argument-hint: "What will the next session focus on?"
---

# Handoff — write STATUS.md

Write (or fully overwrite) `STATUS.md` at the current project root — create it if
absent. It is a SNAPSHOT, not a log: full overwrite every time, never append.
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

- Concrete over narrative: paths, commands, numbers — no prose recap of the
  conversation.
- Nothing secret: no tokens/keys — reference their location instead (e.g.
  "creds in .env").
- If the repo is git-tracked, commit STATUS.md alone with message
  `handoff: <YYYY-MM-DD>` ONLY if the user confirms.
- Re-entry cost must stay under ~2k tokens. If the draft exceeds it, cut
  State/Decisions detail first — never Now/Gotchas.
- Do not duplicate content already captured in other artifacts (BLUEPRINT.md,
  ADRs, PRDs, issues, commits, diffs) — reference them by path in Pointers.
- If the user passed arguments, treat them as what the next session will focus
  on and weight Now accordingly.

## Daybook entry

After STATUS.md is written, append one entry for this session to the project's
daybook, at the path given in the user's global agent instructions (CLAUDE.md /
AGENTS.md). No daybook path configured → skip this step and say so.

The daybook is the opposite of STATUS.md: a LOG, append-only. New entries go at
the bottom; never edit or reorder earlier ones. One file per month
(`YYYY-MM.md`) — create it with a one-line `# Daybook — <project> — <YYYY-MM>`
header if absent. Add the `## <date>` heading only if today's is not already
the last one in the file.

```
## <YYYY-MM-DD> <Day>
### <HH:MM> session — <one-line goal>
- **Did:** …
- **Learned:** …
- **Dead ends:** tried X → failed because Y
- **Debug:** hypothesis → observed value → verdict
- **Parked:** idea unrelated to the task #parked
- **Next:** …
```

- Entries are per session, not per day. No work done → no entry.
- Skip empty fields; do not write "none".
- Items already appended mid-session (parked ideas, dead ends, debug values)
  are not repeated — fold the rest into this entry.
- Same secrets rule as STATUS.md.

## Finish

Tell the user the STATUS.md path and the daybook path, and that the next
session picks STATUS.md up via the CLAUDE.md session-start rule.
