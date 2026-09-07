# agent-skills

Skills for Claude Code, plus Codex CLI mirrors of the five that carry over.
Ten Claude Code skills, five Codex prompts.

## Skills

| Skill | What it does |
|---|---|
| `greenfield` | Bootstraps a new repo with a discipline contract: PRODUCT.md (outcome, opportunity tree, failure modes → eval KPIs, post-ship signals), then BLUEPRINT.md, STATUS.md, REVIEW_LEDGER.md, and a zero-dependency LOC/docstring pre-commit gate. |
| `brownfield` | Same contract retrofitted onto an existing repo. Documents reality, grandfathers oversized files at today's size so they can't grow, never proposes a rewrite. |
| `handoff` | Overwrites STATUS.md with a fixed-section session snapshot (Now / State / Decisions / Gotchas / Pointers) under ~2k tokens, so the next session re-enters in one file-read. |
| `crap-score` | CRAP-metric reduction loop (CC² × (1−cov)³ + CC). Scores every function, then iterates cover-first / split-second until the scorer exits 0. Bundles Python and TS/Node scorers. |
| `optimize-p95` | Profiler-driven latency loop: pick the stack's profiler, attack one hotspot at a time, keep only changes with a measured p95 improvement. |
| `eval-discipline` | The shape of an eval harness: one small Evaluator per KPI, one report column each, independent thresholds, never a blended score. KPI list comes from PRODUCT.md failure modes when present. |
| `design-canon` | Navigation contract for a long-form design manual — read the relevant profile for a structural decision instead of dumping the whole document. |
| `design-taste` | Rules for view transitions, hover states, and motion timing that keep a UI from reading as generic AI output. Includes an anti-slop checklist. |
| `functional-light-js` | Function craft for JS/TS: functions as values, low arity, purity where it pays, composition over flags. |
| `useful-or-cut` | Hostile usefulness filter for prose. Size the piece to the idea, then run a mandatory cut pass expecting 30–50% deletion. Fifteen named slop shapes cut on sight. |

Codex prompts mirror `greenfield`, `brownfield`, `handoff`, `eval-discipline`, and
`crap-score`. They are standalone rewrites, not symlinks — Codex has no subagents or
bundled scripts, so those prompts tell the agent to write the gate rather than copy it.

## Install

Global, both toolchains:

```sh
git clone https://github.com/pktikkani/agent-skills.git
cd agent-skills
./install.sh
```

Copies `claude/skills/*` to `~/.claude/skills/` and `codex/prompts/*.md` to
`~/.codex/prompts/`. Idempotent — re-run to update; same-named skills are replaced,
unrelated ones untouched.

Into one project instead of globally:

```sh
./install.sh --project    # copies to ./.claude/skills (Codex prompts skipped — Codex is global-only)
```

Manually, one skill:

```sh
cp -R claude/skills/handoff ~/.claude/skills/
cp codex/prompts/handoff.md ~/.codex/prompts/
```

## Invocation

**Claude Code.** A skill fires two ways: you type `/handoff`, or the model reads the
`description` line in the frontmatter and invokes it when the work matches. Descriptions
here are written for that second path — `crap-score` and `optimize-p95` say "only when
explicitly invoked" precisely to suppress it. Skills in `~/.claude/skills/` are available
everywhere; `./.claude/skills/` are that project only.

**Codex CLI.** Files in `~/.codex/prompts/` become slash commands by filename:
`greenfield.md` is `/greenfield`. No auto-invocation — you type it.

## Philosophy

Skills are invocation-gated, so only the one-line description sits in context until the
skill actually fires. That makes it cheap to have a dozen installed and pay for none of
them. Loops end at a deterministic gate rather than the model's own judgment — `crap-score`
stops when the scorer exits 0 and `check_discipline.py` blocks the commit, because an
agent asked to decide whether it is finished will say yes. The bundled scripts are
stdlib-only and copy into the target repo, so the gate outlives the agent that installed it.
Every skill assumes the next session starts cold: the artifacts are for the reader who has
no memory of the conversation that produced them.

## Credits

- **CRAP metric** — Alberto Savoia and Bob Martin. `crap-score` implements their formula
  and Bob's worst-first, cover-before-refactor ordering.
- **`functional-light-js`** — distills [Kyle Simpson](https://github.com/getify)'s publicly
  available books, *Functional-Light JavaScript* and *You Don't Know JS*. The books are the
  source; this is a working checklist, not a substitute for reading them.
- **`useful-or-cut`** — the usefulness filter is Shreyas Doshi's flowchart, run in reverse
  against the draft. Six slop shapes and the self-check pattern are adapted from
  [petergyang/no-ai-slop](https://github.com/petergyang/no-ai-slop) (MIT).
- **`handoff`** — the pattern is inspired by Matt Pocock's handoff skill in
  [mattpocock/skills](https://github.com/mattpocock/skills). His pack is worth installing
  alongside this one; it is not vendored here.

MIT licensed. See LICENSE.
