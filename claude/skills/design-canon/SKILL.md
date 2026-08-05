---
name: design-canon
description: Full design-best-practices manual with per-engineer evidence profiles (Hashimoto, Zechner, Ronacher, Dax Raad, Willison). Use when designing architecture, making structural decisions, writing BLUEPRINT.md, or when the user says "design canon" or "check the manual".
---

# Design canon

The always-on core (`~/Documents/design-best-practices.md`) carries only the ten
convergent laws. This skill is for when a decision needs the full evidence, the
reasoning, or a specific engineer's profile.

## How to use it

1. **Read the full manual** at `~/Documents/design-best-practices.md`
   (~1,600 lines — the real manual). Do NOT rely on the distilled core alone for a
   non-trivial structural decision; the evidence and the anti-patterns are what make
   the directives actionable.

   > **Note:** the manual itself is a personal document and is not bundled with this
   > repo. This skill is the navigation contract for it — point it at your own
   > design-principles document (any long-form manual works) by editing the path above.

2. **Navigate, don't dump.** Read the Meta-principles cheat-sheet first, then jump to
   the relevant profile/section for the decision at hand. Each principle is structured
   identically: principle → why it matters → concrete evidence → "As an agent, you
   should…" → the anti-pattern it corrects. The profiles:
   - **Profile 1 — Mitchell Hashimoto** (Ghostty, HashiCorp, libxev): engineering
     discipline, simplest-correct-first, portable core / platform seam, comptime
     binding, one typed schema, config as public contract, data structures from access
     patterns, concurrency (owned config, typed messages, hot-path isolation).
   - **Profile 2 — Mario Zechner** (libGDX, Pi harness): answer-first discipline, terse
     prose, read-to-blast-radius, deletion is confirmation-gated, machine-readable rules.
   - **Profile 3 — Armin Ronacher** (Flask, Jinja2, Click, MiniJinja, insta).
   - **Profile 4 — Dax Raad** (SST, opencode).
   - **Profile 5 — Simon Willison** (Django, Datasette, sqlite-utils, `llm`): leads with
     AI-Assisted Coding — supervise-don't-trust, context-is-king, close-the-loop,
     save-your-prompts. Read his Section A first if you read only one profile section.

3. **Apply the relevant profile/section to the decision**, cite the specific principle
   and its evidence when you justify a design choice, and run the manual's pre-flight
   checklist before finishing a non-trivial change.
