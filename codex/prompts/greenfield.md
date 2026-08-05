# greenfield — bootstrap a new project with a discipline contract

Set up the current (new/empty) repo with a lean architecture contract that a returning
agent (or I, months later) can re-enter in one file-read instead of codebase archaeology.
Generate the files below in the repo root, adapting content to the actual project — do not
paste the examples verbatim. If a file already exists, update it; never clobber real content.

Core loop this enforces: **every session, reread `BLUEPRINT.md` before writing code; update
`STATUS.md` as your last act before ending the session.**

## 1. BLUEPRINT.md — the architecture contract

Written once at project start, updated only by deliberate decision:

- **Stack + why**: the chosen stack in one paragraph, and one alternative noted as a future
  experiment (e.g. "Chose FastAPI for X; revisit Litestar if Y").
- **Folder structure**: an ASCII tree of the intended layout.
- **Module boundaries**: each module with a one-line responsibility. If you can't say it in
  one line, the module is doing too much.
- **Hard limits**: default **400 lines/file, 50 lines/function**. Overridable per project —
  state the numbers explicitly so the gate can read them.
- **Logging discipline** (structured, from day 1): stdlib `logging` (Python) or `pino` (Node).
  Log at decision points (which branch, why) and error boundaries (every except/catch) with
  context values (the ids/inputs that explain the failure), not bare "error occurred".
  Debugging contract: never guess — read the logs. If the logs can't answer it, the first fix
  is adding the logging that would have.
- **Secrets discipline**: secrets live in macOS Keychain; give the project a `.envrc` with
  `export VAR=$(security find-generic-password -a "$USER" -s VAR -w)` lookups (`direnv allow`
  once). Never export secrets in shell rc files; never commit secret values in `.envrc`.
- **The standing rule** (verbatim near the top):
  > Every session: reread this file before writing code. New features conform to this
  > structure, or you update this file FIRST with a dated decision note
  > (`## YYYY-MM-DD — <what changed and why>`).

## 2. STATUS.md — the re-entry doc

The first file a returning agent reads. Updated at the END of every session — your last act:

- **What this is** (2 lines).
- **Current state** (what phase / what's deployed).
- **What works / what doesn't** (honest).
- **Next 3 steps** (concrete, grabbable).
- Footer: `_Last updated: YYYY-MM-DD_`

## 3. scripts/check_discipline.py — the portable gate

Write a zero-dependency (stdlib-only) Python gate at `scripts/check_discipline.py` that,
for each source file under `src/`, `app/`, `lib/`, checks: (a) file LOC ≤ limit, (b) every
function LOC ≤ limit (Python, via `ast`), (c) a module docstring on every Python source file.
It reads limits from BLUEPRINT.md if present (falls back to 400/50) so the gate and the doc
never drift; exits 1 on any violation with a printed list.

Wire it up: a git pre-commit hook (or a `pre-commit` local hook if that framework is in use),
plus `make check` (Python) or a `"check"` npm script (Node). Run it once after scaffolding to
confirm it passes clean.

## 4. Testing policy

- Few high-value tests over coverage theater: contract tests (the public interface holds),
  invariant tests (the thing that must always be true), smoke tests (it boots and does the
  happy path). Skip tests that only restate the implementation.
- Red/green loop for every bug: write the failing test that reproduces it first, watch it
  fail, then fix until green. No fix lands without a test that would have caught it.
- Test file created the same day as the module it covers — not "later".
- AI-feature repos: evals follow the eval-discipline prompt — one Evaluator per KPI, per-column reporting, no blended scores.

## 5. Docs policy

- Every module / class / public function gets a docstring saying WHY it exists (not what the
  code obviously does), readable standalone.
- README stays honest: only document commands that actually work. A README command that fails
  is a bug.

## 6. REVIEW_LEDGER.md — stateful review memory

Stops stateless reviewers from re-discovering the same issues forever. Seed with:

```markdown
# Review Ledger

Every review appends here. Before reviewing: read this ledger, verify open items,
close what's fixed, only THEN add new findings with fresh ids.

| id | date | reviewer | finding | severity | status |
|----|------|----------|---------|----------|--------|
| R1 | YYYY-MM-DD | codex | <finding> | high/med/low | open / fixed / rejected: <reason> |
```

Rule for all reviews: read ledger first → verify each open item (is it actually still
broken?) → close what's fixed / confirm what stands → only then add new findings with fresh
sequential ids. Never re-file an existing finding under a new id.

## Architecture canon — reach for these when a design question arises

Full manual: `~/Documents/design-best-practices.md`. Quick pointers:

- **Fowler — Refactoring / "Monolith First"**: default to one deployable until a seam proves
  itself; don't split into services early.
- **Hickey — "Simple Made Easy"**: choose simple (un-braided, one concept) over easy (close
  at hand, familiar) when a design feels convenient but tangled.
- **Ousterhout — deep modules**: favor deep modules (small interface, large hidden
  implementation) over many shallow pass-throughs.
- **Unix philosophy**: small sharp tools that do one thing and compose via clean interfaces
  when a component starts accreting responsibilities.
