# brownfield — retrofit an existing repo with a discipline contract

Onboard the current repo so a returning agent (or I, months later) can re-enter in one
file-read instead of codebase archaeology. You inherit a codebase with history and must
not break it.

## Core law: ratchet, don't renovate

Document reality first. Freeze decay at today's level. Improve only opportunistically, in
the same commit as work you were already doing. **Never propose a rewrite.**

The repo already works (or half-works) and has a shape someone chose for reasons you may
not see. Make that shape legible and enforced — do not impose the shape it "should" have
had. The BLUEPRINT you write describes the repo **as it is**, warts recorded honestly as
grandfathered facts; the gate ratchets from there — it forbids things getting worse and
lets them get better one file at a time. Structural improvement is a separate, deliberate
future decision, never a big-bang refactor kicked off during onboarding.

Generate the files below in the repo root. If a file exists, update it; never clobber
real content.

## 1. Read the repo first — no writing until you understand it

- **README / docs** — the stated intent (often stale; note where it lies).
- **Entry points** — `main.*`, `app.*`, `index.*`, `manage.py`, `package.json` scripts,
  `Makefile`, `Dockerfile`, and dependency manifests. These reveal the real stack and boot path.
- **Actual structure** — walk the source tree; note real top-level modules and what each
  actually does (not what its name claims).
- **git log** — `git log --oneline -30` and `git log --stat -5` for the shape of recent
  work: what's churning, what's stable, what the last session was mid-way through.
- **Existing decision docs** — `docs/adr/`, `DECISIONS.md`, `CONTEXT.md` if present.

Note every known-bad thing you trip over — you seed the ledger with them in step 6.

## 2. BLUEPRINT.md — reverse-engineered, describing reality

Describe the architecture AS IT IS, not as it should be:

- **Stack + why** (inferred): the actual stack in one paragraph. If the "why" is unknown,
  say so — don't invent a rationale.
- **Folder structure**: an ASCII tree of the actual layout (real top-level dirs, pruned of noise).
- **Module boundaries**: each real module with a one-line responsibility describing what it
  does today. Where a module does too much, say so plainly — it becomes a ledger item, not a rewrite.
- **Data flow**: how a request / job / message actually moves through the system today
  (2-6 bullets or a short ASCII diagram).
- **Hard limits — set to CURRENT reality, grandfathered**:
  - NEW files get the standard **400 lines/file, 50 lines/function**.
  - The largest existing file(s) get a documented, grandfathered cap with a dated note, e.g.:
    > Grandfathered caps (YYYY-MM-DD): `src/legacy/parser.py` capped at 1180 lines (was 1178 at onboarding — do not grow). New files: 400/50.
  - The grandfathered number is a ratchet: the file may not grow past today's size and
    should shrink. It is not a blessing of the size.
- **Logging discipline**: describe what exists today (structured? print-debugging? none?),
  and set the going-forward rule: log at decision points and error boundaries with context
  values. Debugging contract: never guess — read the logs; if the logs can't answer it, the
  first fix is adding the logging that would have.
- **Secrets discipline**: secrets live in macOS Keychain; give the project a `.envrc` with
  `export VAR=$(security find-generic-password -a "$USER" -s VAR -w)` lookups (`direnv allow`
  once). Never export secrets in shell rc files; never commit secret values in `.envrc`.
- **The ratchet rule** (verbatim near the top):
  > Every session: reread this file before writing code. New code fits this structure and the
  > standard 400/50 limits, or you update this file FIRST with a dated decision note
  > (`## YYYY-MM-DD — <what changed and why>`). Grandfathered files may not grow; shrink them
  > when you touch them. Never rewrite what works to match this doc — ratchet, don't renovate.

## 3. AGENTS.md — curated, 15-35 lines

The durable operating facts an agent would make a mistake without. Test each line: would
removing it cause a wrong assumption or a broken command? If not, cut it. Include only:

- One-line what-this-is and who it's for.
- How to run / test / build (commands that actually work — verify them, step 7).
- Non-obvious gotchas that bite (env vars, external services, a fragile step, a "never do X here").
- Pointers: "architecture → BLUEPRINT.md, current state → STATUS.md, open issues → REVIEW_LEDGER.md".

Keep it 15-35 lines. Longer means it won't be read.

## 4. STATUS.md — the re-entry doc

The first file a returning agent reads. Short and honest:

- **What this is** (2 lines).
- **Current state** (what phase / what's deployed / what the last commit was doing).
- **What works / what's broken** (honest — warts go here).
- **Next 3 steps** (concrete, grabbable).
- Footer: `_Last updated: YYYY-MM-DD_`

## 5. scripts/check_discipline.py — the gate, honoring grandfather overrides

Write a zero-dependency (stdlib-only) Python gate at `scripts/check_discipline.py` that,
for each source file under `src/`, `app/`, `lib/`:

1. Checks file LOC against its cap — a per-file **grandfathered cap** if BLUEPRINT.md lists
   one for it (as `` `path` capped at N lines ``), otherwise the global 400.
2. Checks every function is ≤ 50 lines (Python, via `ast`).
3. Checks every Python module has a module docstring.

Adapt the source roots it scans to the repo's real layout (e.g. `services/`, `packages/`,
`apps/` for a monorepo). On an established Python codebase, checks 2-3 fire on dozens of
legacy functions — grandfathering can't cover individual functions, so add a `--loc-only`
flag that enforces only the god-file LOC freeze (the real ratchet) and skips the
function/docstring checks; wire the hook to use it, and track the function-length /
missing-docstring debt as ledger items to pay down when those files are touched.

It reads the global limits and the grandfathered caps from BLUEPRINT.md so the gate and the
doc never drift; exits 1 on any violation with a printed list. Wire it up: a git pre-commit
hook (or a `pre-commit` local hook if that framework is in use), plus `make check` (Python)
or a `"check"` npm script (Node). Run it once, read every file it flags, and **grandfather
all of them at today's size** in the BLUEPRINT caps block — a hook that always fails is
useless as a ratchet, so the gate must pass NOW with every current over-limit file frozen so
none may grow and all should shrink. Grandfathering is a freeze, NOT a blessing: record the
debt in the ledger, flagging the worst god-files as higher severity to shrink first. Do NOT
fix any of them now.

## 6. REVIEW_LEDGER.md — seeded with what you found

Seed with the known-bad things you tripped over while reading and the non-grandfathered gate
violations worth tracking. Each starts `status=open`.

```markdown
# Review Ledger

Every review appends here. Before reviewing: read this ledger, verify open items,
close what's fixed, only THEN add new findings with fresh ids.

| id | date | reviewer | finding | severity | status |
|----|------|----------|---------|----------|--------|
| R1 | YYYY-MM-DD | codex | <finding found during onboarding> | high/med/low | open |
```

## 7. Tests — verify or bootstrap one smoke check

- If the repo has tests: find the entry point (`pytest`, `npm test`), run it, record the
  working command in AGENTS.md. If broken, that's a ledger item — don't fix a whole suite now.
- If the repo has zero tests: write ONE runnable smoke check (boots the app / imports the
  package / hits the happy path) and document its run command in AGENTS.md.
- AI-feature repos: any evals you add follow the eval-discipline prompt — one Evaluator per
  KPI, per-column reporting, no blended scores (a ledger item if the existing suite blends).

## 8. Report back

- **Documented**: the files written.
- **Grandfathered**: which file(s) got a grandfathered cap and at what size.
- **Riskiest thing found**: the single most dangerous issue uncovered while reading.

## What NOT to do

- Do not propose or start a rewrite, re-architecture, or framework swap. If the repo "should"
  be structured differently, that's a ledger item for a future deliberate decision.
- Do not fix existing gate violations in bulk. Grandfather the largest, track the rest, move on.
- Do not invent a rationale you can't explain. "Why unknown" is an honest BLUEPRINT entry.
- Do not clobber existing README/docs — fold and preserve.
