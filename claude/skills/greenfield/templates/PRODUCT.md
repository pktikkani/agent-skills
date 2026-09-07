# PRODUCT — <project name>

> Written before BLUEPRINT.md. Reread every session with it. Change the outcome only by a
> dated note at the bottom. Rule: **every roadmap line names the opportunity or failure mode
> it serves. No line, no build.**

## Outcome
<the ONE number the customer judges us on> — today: <value> → target: <value> by <date>.
Measured by: <how, from whose data>.

## User
<who, in one line: role, context, what a bad week looks like for them>

## Opportunity tree
Outcome ← opportunities (user's words) ← solutions ← assumptions to test

- O1 <opportunity / pain, quoted or paraphrased from a real user>
  - S1a <solution> — assumes: <what must be true>
- O2 …
- O3 …

## Failure modes (ranked; these are the eval KPIs)
| id | failure mode | why it breaks the outcome |
|----|--------------|---------------------------|
| F1 | <e.g. invented commitment> | <e.g. user distrusts every nudge after one wrong one> |
| F2 | <e.g. wrong owner> | … |
| F3 | … | … |

## Pre-ship evidence
| failure mode | dataset | evaluator (name = report column) | threshold to ship |
|--------------|---------|----------------------------------|-------------------|
| F1 | <n labelled items, path> | `<evaluator_name>` | <e.g. ≤2% of extracted items> |

## Post-ship signals
| failure mode | signal (same name as evaluator) | how observed in prod |
|--------------|---------------------------------|----------------------|
| F1 | `<evaluator_name>` | <event / user action / field> |

## Discovery cadence
Weekly <n>-min interview with <who>; notes in `docs/discovery/YYYY-MM-DD.md`.
Question we are trying to answer this month: <one line>.

## Decision log
- <YYYY-MM-DD> — initial outcome set.
