---
name: brownfield
description: Retrofit an EXISTING repo with a lean discipline contract — document reality, freeze decay, improve opportunistically. Use when onboarding an inherited or old codebase, or when the user says "onboard this repo", "brownfield", "retrofit", or "bring this old project under discipline".
---

# Brownfield

Retrofit an existing repo with the same discipline contract `/greenfield` gives a new one, so a returning agent (or you, months later) can re-enter in one file-read instead of codebase archaeology. The difference from greenfield: **you inherit a codebase with history, and you must not break it.**

## Core law: ratchet, don't renovate

> Document reality first. Freeze decay at today's level. Improve only opportunistically, in the same commit as work you were already doing. **Never propose a rewrite.**

A brownfield repo already works (or half-works) and has a shape someone chose for reasons you may not see. Your job is to make that shape *legible and enforced*, not to impose the shape it "should" have had. The BLUEPRINT you write describes the repo **as it is** — including its warts, recorded honestly as grandfathered facts — and the gate you install ratchets from *there*: it forbids things getting worse, and lets them get better one file at a time. Any structural improvement is a separate, deliberate decision the returning agent makes with eyes open, never a big-bang refactor you kick off during onboarding.

Generate the files below **in the repo's root**. If a file already exists, update it; never clobber real content.

## 1. Read the repo first — no writing until you understand it

Reverse-engineering an honest BLUEPRINT is impossible without reading. Spend the first block of time reading, not writing:

- **README / docs** — the stated intent (often stale; note where it lies).
- **Entry points** — `main.*`, `app.*`, `index.*`, `manage.py`, `package.json` `scripts`, `Makefile`, `Dockerfile`, `pyproject.toml`/`requirements.txt`/`package.json` deps. These tell you the real stack and how it boots.
- **Actual structure** — walk the source tree; note the real top-level modules and what each *actually* does (not what its name claims).
- **git log** — `git log --oneline -30` and `git log --stat -5` for the shape of recent work: what's churning, what's stable, what the last agent was mid-way through.
- **Auto-memory** — if `~/.claude/projects/<encoded-path>/memory/` exists for this repo, read it. `<encoded-path>` is the repo's absolute path with `/` replaced by `-` (e.g. `/Users/me/x/foo` → `-Users-me-x-foo`). Durable facts there (decisions, gotchas, org context) are promotion candidates for AGENTS.md.
- **Existing ADRs / decision docs** — `docs/adr/`, `DECISIONS.md`, `CONTEXT.md` if present.

Note every known-bad thing you trip over while reading — you will seed the ledger with them in step 6.

## 2. BLUEPRINT.md — reverse-engineered, describing reality

Written to describe the architecture **AS IT IS**, not as it should be. Contains:

- **Stack + why** (inferred): the actual stack in one paragraph. If the "why" is unknown, say so — don't invent a rationale.
- **Folder structure**: an ASCII tree of the **actual** layout (the real top-level dirs, pruned of noise).
- **Module boundaries**: each real module/package with a one-line responsibility describing what it *actually does today*. Where a module does too much, say that plainly — it becomes a ledger item, not a rewrite. **One-module test, in reverse** (orthogonality, /design-canon Profile 6 A2): pick 2-3 recent commits from `git log --stat` and 2-3 likely future changes, and record how many modules each touches. A small change that spreads across unrelated modules, or shared module-level globals, is recorded as a coupling ledger item — not fixed now.
- **Homes for facts — as found** (DRY, /design-canon Profile 6 A1): list the facts that live in more than one place today (hand-written types mirroring an API or DB schema, constants repeated across files, near-duplicate helpers, a derived value stored beside its source). For each, name which copy is authoritative *today*. Every multi-home fact becomes a ledger item; new code uses the authoritative copy and adds no further mirror.
- **Data flow**: how a request / job / message actually moves through the system today (2-6 bullets or a short ASCII diagram).
- **Hard limits — set to CURRENT reality, grandfathered**:
  - **NEW files** get the standard **400 lines/file, 50 lines/function**.
  - The **largest existing file** becomes a documented, grandfathered cap. Record it as a per-file override with a dated note, e.g.:
    > Grandfathered caps (2026-07-18): `src/legacy/parser.py` capped at 1180 lines (was 1178 at onboarding — do not grow). New files: 400/50.
  - The point of the grandfathered number is a **ratchet**: the file may not grow past today's size, and should shrink. It is not a blessing of the size.
- **Logging discipline**: describe what exists today (structured? print-debugging? none?), and set the going-forward rule: log at decision points and error boundaries with context values. Debugging contract: **never guess — read the logs**; if the logs can't answer it, the first fix is to add the logging that would have.
- **Secrets discipline**: secrets live in macOS Keychain; give the project a `.envrc` with `export VAR=$(security find-generic-password -a "$USER" -s VAR -w)` lookups (`direnv allow` once). Never export secrets in shell rc files; never commit secret values in `.envrc` (existing `.env` files stay as-is).
- **The ratchet rule** (put this verbatim near the top):
  > Every session: reread this file before writing code. New code fits this structure and the standard 400/50 limits, or you update this file FIRST with a dated decision note (`## YYYY-MM-DD — <what changed and why>`). Grandfathered files may not grow; shrink them when you touch them. Never rewrite what works to match this doc — ratchet, don't renovate.

## 3. AGENTS.md — curated, 15-35 lines

The durable operating facts an agent needs and would make a mistake without. **Test for each line: would removing this cause a wrong assumption or a broken command?** If not, cut it. Promote durable facts from auto-memory and ADRs here (the raw memory files stay; AGENTS.md is the curated distillation). Include only:

- One-line what-this-is and who it's for.
- How to run / test / build (the commands that actually work — verify them, see step 7).
- Non-obvious gotchas that bite (env vars, external services, a fragile step, a "never do X here").
- Pointers: "architecture → BLUEPRINT.md, current state → STATUS.md, open issues → REVIEW_LEDGER.md".

Keep it 15-35 lines. Longer means it won't be read. Then make `CLAUDE.md` a single line so both toolchains resolve to one source:

```
@AGENTS.md
```

If `CLAUDE.md` already has real content, fold the durable bits into AGENTS.md first, then replace it with `@AGENTS.md`.

## 4. STATUS.md — the re-entry doc

The single file a returning agent reads first. Keep it short and honest:

- **What this is** (2 lines).
- **Current state** (what phase / what's deployed / what the last commit was doing).
- **What works / what's broken** (honest — this is where the warts go).
- **Next 3 steps** (concrete, grabbable).
- Footer: `_Last updated: YYYY-MM-DD by <agent/you>_`

## 5. scripts/check_discipline.py — the gate, honoring grandfather overrides

Copy `scripts/check_discipline.py` from this skill's bundle into the repo's `scripts/`. It is zero-dependency (stdlib only), reads the standard 400/50 limits from BLUEPRINT.md, **and honors per-file grandfather overrides** declared as `` `path/to/file` capped at N lines `` lines in BLUEPRINT.md (each listed file is checked against its own cap instead of the global limit). Adapt `SRC_DIRS` at the top of the script to the repo's real source roots (e.g. `["services", "packages", "apps"]` for a monorepo) and extend `PY_EXCLUDE_DIRS` to skip test/generated/vendored trees.

The gate also checks Python function length (50) and module docstrings. On an established Python codebase these fire on dozens of legacy functions — grandfathering can't cover individual functions, so a gate that enforces them blocks every commit and breaks the ratchet. In that case run the gate with **`--loc-only`**: it enforces the god-file LOC freeze (the real ratchet) and *skips* the function/docstring checks. Track the function-length and missing-docstring debt as ledger items instead, to be paid down opportunistically when those files are touched. Reserve full-strictness (no `--loc-only`) for repos clean enough to pass it.

Wire it up:
- **If git**: install as a pre-commit hook (`.git/hooks/pre-commit` calling `python scripts/check_discipline.py`, chmod +x). If `pre-commit` framework is in use, add a local hook instead.
- **Per convention**: add `make check` (Python) or a `"check"` npm script (Node).
- **Run it once**, read the list of every file it flags, and **grandfather all of them at today's size** in the BLUEPRINT caps block. This is the freeze line: a pre-commit hook that always fails is useless as a ratchet, so the gate must pass *now* — with every current over-limit file frozen so none may grow and all should shrink. Grandfathering is a freeze, **not** a blessing: record the debt in the ledger (step 6), calling out the genuinely worst files (the god-files) as higher-severity items to shrink first. Do **not** fix any of them now.

## 6. REVIEW_LEDGER.md — seeded with what you found

Seed the ledger with the known-bad things you tripped over while reading (step 1) and the non-grandfathered gate violations worth tracking. Each starts `status=open`.

```markdown
# Review Ledger

Every review appends here. **Before reviewing: read this ledger, verify open items,
close what's fixed, only THEN add new findings with fresh ids.**

| id | date | reviewer | finding | severity | status |
|----|------|----------|---------|----------|--------|
| R1 | YYYY-MM-DD | claude | <finding found during onboarding> | high/med/low | open |

## Standing checks — run on every review
- **DRY**: a hand-written copy of a schema / API type / constant / rule that has a home in BLUEPRINT.md, or a near-duplicate helper → finding. (/design-canon Profile 6 A1)
- **Orthogonality**: a diff spreading across unrelated modules, a new module-level global, reaching into another module's internals, or a test that needs global resets → coupling finding. (Profile 6 A2)
```

Standing checks apply to **new and touched code** (ratchet law): existing duplication and coupling are the seeded ledger items above, paid down opportunistically — never a bulk cleanup.

Rule for all reviews (also in global CLAUDE.md): read ledger first → verify each open item → close what's fixed → only then add new findings with fresh ids. Never re-file an existing finding under a new id.

## 7. Tests — verify or bootstrap one smoke check

- **If the repo has tests**: find the test entry point (`pytest`, `npm test`, etc.), run it, and record the working command in AGENTS.md. If it's broken, that's a ledger item — note it, don't fix a whole suite during onboarding.
- **If the repo has zero tests**: write **one** runnable smoke check — boots the app / imports the package / hits the happy path — and document its run command in AGENTS.md. One real smoke test beats a coverage plan you won't execute.
- **If it's an AI-feature repo**: any evals you add follow **/eval-discipline** — one Evaluator per KPI, per-column reporting, no blended scores (a ledger item if the existing suite blends).

## 8. Report back

End with a tight report:

- **Documented**: the files written (BLUEPRINT / AGENTS / STATUS / ledger / gate / smoke test).
- **Grandfathered**: which file(s) got a grandfathered cap and at what size.
- **Riskiest thing found**: the single most dangerous issue uncovered while reading — the one to look at first.

## What NOT to do

- Do **not** propose or start a rewrite, re-architecture, or framework swap. If the repo "should" be structured differently, that's a ledger item for a future deliberate decision, not onboarding work.
- Do **not** fix existing gate violations in bulk. Grandfather the largest, track the rest, move on.
- Do **not** invent a rationale for a choice you can't explain. "Why unknown" is an honest and useful BLUEPRINT entry.
- Do **not** clobber existing README/CLAUDE/docs content — fold and preserve.

## Architecture canon

When a structural question arises during onboarding, consult **/design-canon** (full manual at `~/Documents/design-best-practices.md`) — but remember the ratchet law overrides the urge to apply it retroactively. The canon guides *new* code and *deliberate* future refactors, not a big-bang cleanup of what already ships.

Language craft: if the repo is JavaScript/TypeScript, invoke the
**functional-light-js** skill when writing NEW code in it (ratchet law: it
guides new functions and deliberate refactors, never a bulk cleanup of what
already ships).

## Bundled files

- `scripts/check_discipline.py` — copy into the repo's `scripts/`.
