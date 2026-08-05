---
name: functional-light-js
description: Kyle Simpson's (getify) function craft from Functional-Light JS and You Don't Know JS. Use when writing or reviewing JavaScript/TypeScript functions, refactoring JS/TS code, or when the user mentions first-class functions, functional-light, or getify/Kyle Simpson.
---

# Functional-Light JS (Kyle Simpson)

Core stance: FP for **readability**, not purity dogma. A technique earns its
place only if the next reader trusts the code more because of it.

## Function craft

- **Functions are values.** Assign them, pass them, return them; design APIs
  that accept and return functions rather than flags and modes.
- **Name every function.** Named function expressions over anonymous arrows
  for anything non-trivial — names document intent and appear in stack
  traces. An arrow is fine only when the whole body is self-evident.
- **Keep arity low.** Prefer unary/binary. Three+ related args → single
  options object. Specialize with partial application / currying instead of
  adding parameters.
- **Pure by default.** Same input → same output, no observed side effects.
  Push side effects to the edges (matches the pure-core/IO-shell rule);
  where a side effect is unavoidable, make it obvious, not buried.
- **Immutability as discipline:** return new values instead of mutating
  arguments; treat received data as read-only even when the language won't
  enforce it.
- **Composition over orchestration.** Build behavior from small composed
  functions (`pipe`/`compose`); each piece independently nameable and
  testable.
- **Closure over `this`.** Capture state with closures; use `this` only for
  genuine method polymorphism, and never implicitly rebind it.

## Readability guardrails (the "-light" part)

- Declarative `map`/`filter`/`reduce` when it reads clearer — but a plain
  loop beats a clever `reduce`. Never stack transformations the reader must
  mentally unroll.
- Point-free style only when it removes noise; if the reader must
  reconstruct the missing argument, write it out.
- Don't import a heavy FP library for two helpers; write the small utility
  and name it well.
- Understand coercion and use it deliberately (`==` where types are known
  and intended) rather than cargo-culting `===` everywhere — but in shared
  codebases, follow the house style.

## Review checklist

When reviewing JS/TS, flag: anonymous multi-line callbacks, functions >3
args, hidden mutation of parameters, side effects mid-pipeline, `this`
passed through bind-chains, and clever one-liners that need unrolling.

## Audit mode (manual — user says "kyle audit" / "functional-light audit")

Sweep the repo's JS/TS against the checklist as a periodic gate:

1. Inventory findings per file (checklist item, file:line, one-line quote).
   Cheap first pass with rg (e.g. arrow callbacks spanning lines, `function
   \w+\(.*,.*,.*,` for arity, `\.push\(`/`Object.assign` on params); then
   read the flagged files to confirm — no regex-only verdicts.
2. Write the full findings table to a report file; reply with path, counts
   per category, and the 5 worst offenders.
3. If the user says fix: role hierarchy applies — one finding-cluster per
   Opus dev instruction, tests green after each, full re-sweep at the end.
   Unforgiving mode: no scope-shrinking, re-audit output pasted in report.
