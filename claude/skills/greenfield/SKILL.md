---
name: greenfield
description: Bootstrap a new project with a lean architecture contract. Use when creating a new project / repo from scratch, scaffolding a codebase, or when the user says "new project", "greenfield", "start a repo", or "set up a project skeleton".
---

# Greenfield

Bootstrap a new repo with a discipline contract that a returning agent (or you, months later) can re-enter in one file-read instead of codebase archaeology. Generate the files below **in the new repo's root** (adapt content to the actual project — do not paste the examples verbatim). If a file already exists, update it; never clobber real content.

Core loop this skill enforces: **`PRODUCT.md` is written before `BLUEPRINT.md`; every session, reread both before writing code; update `STATUS.md` as your last act before ending the session.**

## 0. PRODUCT.md — the product contract (written FIRST)

The layer above architecture. Locks *what success is* before anything is designed, so that
evals, telemetry and the roadmap all trace to one outcome. Copy `templates/PRODUCT.md` from this
skill's bundle and fill it in with the human — never invent the outcome. Contains, in order:

- **Outcome**: the ONE number the customer will judge the product on, with today's value and
  the target (e.g. "commitments closed by due date: 40% → 70% in 90 days"). One outcome per
  product; more is a sign of no decision.
- **User + opportunity tree** (Teresa Torres): who the user is, and 3-5 *opportunities*
  (unmet needs / pains, in the user's words) that block the outcome. Solutions hang under
  opportunities; each solution lists the **assumption** that must hold for it to work.
- **Failure modes**: what would make the outcome fail even if the code is correct, ranked.
  For AI features these are things like "invented commitment", "wrong owner", "wrong date".
  **These ARE the eval KPIs** — /eval-discipline reads this list; one evaluator per row.
- **Pre-ship evidence**: for each failure mode, how it is measured before deploy (labelled
  dataset + evaluator name + threshold). No threshold → not shippable.
- **Post-ship signals**: for each failure mode, how it is observed in production (the event,
  the user action, the field). **Same name as the eval column** so a prod drop points to the
  eval to rerun. This is the telemetry spec — design it in, don't bolt it on.
- **Discovery cadence**: the weekly touchpoint with a real user (Torres: interview, not
  survey) and where notes land (`docs/discovery/YYYY-MM-DD.md`).
- **Traceability rule** (verbatim): *Every `## Roadmap` line in BLUEPRINT.md names the
  opportunity or failure mode it serves. No line, no build.*

Changes to the outcome are rare and dated (`## YYYY-MM-DD — outcome changed because …`),
same as BLUEPRINT.md decision notes.

## 1. BLUEPRINT.md — the architecture contract

Written once at project start, updated only by deliberate decision. Contains:

- **Stack + why**: the chosen stack in one paragraph, and *one* alternative noted as a future experiment (e.g. "Chose FastAPI for X; revisit Litestar if Y").
- **Folder structure**: an ASCII tree of the intended layout.
- **Module boundaries**: each module/package with a one-line responsibility. If you can't say it in one line, the module is doing too much.
- **Hard limits**: default **400 lines/file for code, 50 lines/function**. Overridable per project — state the numbers explicitly so the gate can read them.
- **Roadmap**: `## Roadmap` — one line per planned feature, held loosely (reorder freely as STATUS.md learns). **Delete lines when shipped** — STATUS records what's done; this section is a queue, never a log. Features are pulled from here one at a time into the /tdd loop. **Each line ends with `→ <opportunity or failure mode from PRODUCT.md>`** (traceability rule).
- **Logging discipline** (structured, from day 1): stdlib `logging` (Python) or `pino` (Node). Log at **decision points** (which branch, why) and **error boundaries** (every `except`/`catch`) with **context values** (the ids/inputs that explain the failure), not bare "error occurred". Debugging contract: **never guess — read the logs.** If the logs can't answer the question, the first fix is to add the logging that would have.
- **Secrets discipline**: secrets live in macOS Keychain; give the project a `.envrc` with `export VAR=$(security find-generic-password -a "$USER" -s VAR -w)` lookups (`direnv allow` once). Never export secrets in shell rc files; never commit secret values in `.envrc`.
- **The standing rule** (put this verbatim near the top):
  > Every session: reread this file before writing code. New features conform to this structure, or you update this file FIRST with a dated decision note (`## YYYY-MM-DD — <what changed and why>`).

## 2. STATUS.md — the re-entry doc

The single file a returning agent reads first. Updated at the **END of every working session — the agent's last act.** Keep it short:

- **What this is** (2 lines).
- **Current state** (what phase / what's deployed).
- **What works / what doesn't** (honest).
- **Next 3 steps** (concrete, grabbable).
- Footer: `_Last updated: YYYY-MM-DD by <agent/you>_`

Purpose: returning after months costs one file-read, not archaeology.

## 3. scripts/check_discipline.py — the portable gate

Copy `scripts/check_discipline.py` from this skill's bundle into the new repo. It is **zero-dependency** (stdlib only) and checks: (a) file LOC limits, (b) function LOC limits, (c) a module docstring on every source file. It reads limits from `BLUEPRINT.md` if present (falls back to 400/50).

Wire it up:
- **If the repo has git**: install as a pre-commit hook (`.git/hooks/pre-commit` calling `python scripts/check_discipline.py`, chmod +x). If `pre-commit` framework is in use, add a local hook instead.
- **Per repo convention**: add `make check` (Makefile) for Python, or a `"check"` npm script for Node, that runs the gate. Run it once after scaffolding to confirm it passes clean.

## 4. Testing policy

- **Few high-value tests over coverage theater**: contract tests (the public interface holds), invariant tests (the thing that must always be true), smoke tests (it boots and does the happy path). Skip tests that only restate the implementation.
- **Red/green loop for every bug**: write the failing test that reproduces it *first*, watch it fail (red), then fix until green. No fix lands without a test that would have caught it.
- **Feature dev runs /tdd with the red gate**: contract-defining tests are shown to the human at RED (failing) for approval before implementation — the test is the spec.
- **Invariants get a property test** (hypothesis / fast-check) where a generator is cheap to write — mechanize the invariant instead of hand-picking examples. Mutation testing and fuzzing are NOT default: mutation only as an occasional audit of critical modules; fuzz only for code parsing untrusted input.
- **Test file created the same day** as the module it covers — not "later".
- **AI-feature repos**: evals follow **/eval-discipline** — one Evaluator per KPI, per-column reporting, no blended scores. The KPI list IS `PRODUCT.md` → Failure modes; evaluator names match the post-ship signal names.

## 5. Docs policy

- Every **module / class / public function** gets a docstring saying **WHY it exists** (not what the code obviously does), readable standalone.
- **README stays honest**: only document commands that actually work. A command in the README that fails is a bug.

## 6. REVIEW_LEDGER.md — stateful review memory

Stops stateless reviewers (Claude, Codex) from re-discovering the same issues forever. Seed the new repo with:

```markdown
# Review Ledger

Every review appends here. **Before reviewing: read this ledger, verify open items,
close what's fixed, only THEN add new findings with fresh ids.**

| id | date | reviewer | finding | severity | status |
|----|------|----------|---------|----------|--------|
| R1 | YYYY-MM-DD | claude | <finding> | high/med/low | open / fixed / rejected: <reason> |
```

Rule for **all** reviews (also in global CLAUDE.md): read ledger first → verify each open item (is it actually still broken?) → close what's fixed / confirm what stands → only then add new findings with fresh sequential ids. Never re-file an existing finding under a new id.

## Architecture canon — reach for these when a design question arises

During blueprint drafting, consult **/design-canon** (full manual at
`~/Documents/design-best-practices.md`) — the convergent laws and
per-engineer evidence for structural decisions. The classics below stay as quick
one-line pointers:

- **Fowler — Refactoring / "Monolith First"**: when tempted to split into services early, or when a module has grown messy but you're unsure how to carve it. Default to one deployable until a seam proves itself.
- **Hickey — "Simple Made Easy"**: when a design feels convenient but tangled. Choose *simple* (un-braided, one concept) over *easy* (close at hand, familiar).
- **Ousterhout — *A Philosophy of Software Design* (deep modules)**: when defining a module boundary. Favor deep modules — small interface, large hidden implementation — over many shallow pass-throughs.
- **Unix philosophy**: when a component is accreting responsibilities. Make small sharp tools that do one thing and compose via clean interfaces.

Language craft: if the stack is JavaScript/TypeScript, invoke the
**functional-light-js** skill before writing implementation code and apply it
throughout (function craft: naming, arity, purity, composition).

## Bundled files

- `scripts/check_discipline.py` — copy into the new repo's `scripts/`.
- `templates/PRODUCT.md` — copy to the new repo's root and fill in with the human before BLUEPRINT.md.
