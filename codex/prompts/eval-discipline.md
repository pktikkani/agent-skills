# eval-discipline — how to write evals and build an eval harness

How to structure the evals themselves: KPI-based evaluators, per-column reporting, no
blended scores. Use when writing evals, building an eval harness, adding evals to an AI
feature, or scoring a pipeline. This governs the *shape* of the evaluators and the report;
pair it with your error-analysis / judge-validation workflows, which it does not replace.

## Directives

- **The KPI list comes from `PRODUCT.md` when it exists.** Its *Failure modes* table is the
  evaluator list — one Evaluator per row, `name` equal to the row's post-ship signal name so a
  production drop maps straight to the eval to rerun. Thresholds come from *Pre-ship evidence*.
  A column with no row in PRODUCT.md is ornamental until the human adds the row.
- **KPI-based, never generic.** Every evaluator traces to a real failure mode (found via
  error analysis) or a business KPI. Ten meaningful columns beat thirty ornamental ones. If
  you can't name the failure mode or KPI a column defends, don't add it.
- **One small Evaluator per KPI — never a mega-scorer.** Each is a tiny class with a uniform
  minimal interface (`name`, `evaluate(trace, ctx) -> Score`). The harness composes them;
  adding, deleting, or re-tuning one never touches another.
- **Report the vector, never a blend.** Every KPI is its own column; regressions are tracked
  per column and gated with **independent thresholds**. NEVER collapse into one blended
  quality score for decisions — a mean hides the regression that matters.
- **Shared preprocessing computed once.** Parse/normalize the trace one time into a context
  object (`ctx`) passed to all evaluators. Never re-parse the trace N times.
- **Right tool per KPI.** Deterministic code-check wherever the KPI is checkable (schema,
  latency, exact rules, presence/format). Reserve an **LLM judge** for KPIs where
  interpretation is unavoidable (tone, faithfulness, relevance).
- **Every judge is calibrated before it's trusted.** An LLM judge earns its column only after
  being validated against human labels (TPR/TNR). An uncalibrated judge is a guess with a
  number on it.
- **Deletion and tightening are surgery-free.** Removing a dead metric drops one class and one
  column. Tightening one gate changes one threshold. If either forces you to re-tune others,
  the evaluators are entangled — split them.

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

TS equivalent: `interface Evaluator { name: string; evaluate(trace, ctx): Score }` with
`Score = { value: number | boolean; reasons?: string[] }`.

The harness builds `ctx` once, runs each evaluator, and emits one column per `name`.

## Reference exemplar

A prose-critic harness with `slop`, `discourse`, and `spectral` as three separate small
judges, each with its own column — not one blended "writing quality" score. Copy that shape.

## Workflow pairing

Precede this with error analysis (to find the failure modes each column defends) and judge
validation (calibrate every LLM judge against human labels via TPR/TNR before trusting its
verdicts). This skill assumes those workflows exist; it defines the evaluator/report shape
they feed into.
