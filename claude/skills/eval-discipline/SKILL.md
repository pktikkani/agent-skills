---
name: eval-discipline
description: How to write evals and build an eval harness the disciplined way — KPI-based evaluators, per-column reporting, no blended scores. Use when writing evals, building an eval harness, when the user says "add evals", "score this pipeline", or asks about KPI evaluation of an AI feature.
---

# Eval discipline

How to structure the evals themselves. This complements the **evals-skills** pack
(hamel's) — that pack covers the *workflows* (error-analysis, judge validation,
synthetic data); this skill governs the *shape* of the evaluators and the report.

## Directives

- **KPI-based, never generic.** Every evaluator traces to a real failure mode (found
  via error analysis) or a business KPI. Ten meaningful columns beat thirty ornamental
  ones. If you can't name the failure mode or KPI a column defends, don't add it.
- **One small Evaluator per KPI — never a mega-scorer.** Each is a tiny class with a
  uniform minimal interface (`name`, `evaluate(trace, ctx) -> Score`). The harness
  composes them; adding, deleting, or re-tuning one never touches another.
- **Report the vector, never a blend.** Every KPI is its own column in the report;
  regressions are tracked per column and gated with **independent thresholds**. NEVER
  collapse into one blended quality score for decisions — a mean hides the regression
  that matters.
- **Shared preprocessing computed once.** Parse/normalize the trace one time into a
  context object (`ctx`) passed to all evaluators. Never re-parse the trace N times.
- **Right tool per KPI.** Use a deterministic code-check wherever the KPI is checkable
  (schema, latency, exact rules, presence/format). Reserve an **LLM judge** for KPIs
  where interpretation is unavoidable (tone, faithfulness, relevance).
- **Every judge is calibrated before it's trusted.** An LLM judge earns its column only
  after being validated against human labels (TPR/TNR) — see the evals-skills
  **validate-evaluator** skill for the how. An uncalibrated judge is a guess with a
  number on it.
- **Deletion and tightening are surgery-free.** Removing a dead metric drops one class
  and one column. Tightening one gate changes one threshold. If either forces you to
  re-tune others, the evaluators are entangled — split them.

## Evaluator interface (language-agnostic sketch)

```python
@dataclass
class Score:
    value: float | bool          # the KPI's measurement
    reasons: list[str] = ()      # optional: why (judge rationale, failing rule)

class Evaluator(Protocol):
    name: str                            # -> the report column header
    def evaluate(self, trace, ctx) -> Score: ...
```

TS equivalent: `interface Evaluator { name: string; evaluate(trace, ctx): Score }`
with `Score = { value: number | boolean; reasons?: string[] }`.

The harness builds `ctx` once, runs each evaluator, and emits one column per `name`.

## Reference exemplar

A prose-critic harness with `slop`, `discourse`, and `spectral` as three separate
small judges, each with its own column — not one blended "writing quality" score.
Copy that shape.

## Workflow pointers (evals-skills pack)

- Finding the failure modes that justify each column → **error-analysis** skill.
- Writing an LLM judge for an interpretive KPI → **write-judge-prompt** skill.
- Calibrating that judge against human labels before trusting it → **validate-evaluator** skill.
- Auditing an existing eval suite for vanity metrics / unvalidated judges → **eval-audit** skill.
