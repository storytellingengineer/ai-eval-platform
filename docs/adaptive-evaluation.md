# Adaptive Evaluation Pipeline

## Purpose

The adaptive evaluation pipeline separates three responsibilities:

1. Jev decision layer — decides which evaluation dimensions are relevant.
2. Evaluator implementations — perform the actual quality and safety checks.
3. Observability adapter — records decisions and evaluator results in Langfuse or another tracing system.

The key design goal is risk-aware specialization, not simply reducing evaluator cost.

## Flow

Trace / Observation
    |
    v
Jev Decision Layer
    |
    v
Evaluation Plan
    |
    +----> relevance
    +----> groundedness
    +----> tool correctness
    +----> PII / toxicity / other registered evaluators
    |
    v
Evaluation Results
    |
    v
Langfuse / Observability

The AdaptiveEvaluationPipeline implements the missing execution step between routing and observability.

## Why the execution layer matters

The earlier POC proved that a decision can be produced and validated against a controlled evaluator registry. That is not enough for a production architecture: selected evaluators must actually run and their results must be emitted.

The executor therefore:

- asks the decision engine for an EvaluationPlan;
- executes only selected evaluator implementations;
- validates that each result reports the evaluator name that was selected;
- fails fast when routing selects an evaluator that has no implementation;
- keeps evaluator implementations independent from Jev and Langfuse.

This makes the layer usable with deterministic metrics, LLM-as-a-judge evaluators, or future agent/RAG evaluators.

## Evaluation strategy

Do not claim that adaptive routing improves quality until it is measured.

For a meaningful experiment, compare:

- Baseline: every configured evaluator runs on every trace.
- Adaptive: Jev selects the relevant evaluator set.

Primary quality metrics:

- issue/defect recall;
- missed-issue rate;
- evaluator coverage;
- false-selection rate.

Operational metrics:

- evaluator executions;
- routing latency;
- end-to-end latency;
- model/token cost where applicable.

The central research question is:

Can evaluation be specialized by trace risk and context without materially reducing defect detection?

## Production integration

The executor accepts provider-independent callables of the form:

dict[str, Callable[[TraceSnapshot], MetricResult]]

A production integration can register LLM judges or other evaluators under the same names and then use the existing Langfuse score helper to publish the plan and individual results.

The local DemoJevDecisionModel is deliberately deterministic. It is a test/demo adapter, not evidence of Jev routing quality. Replace it with TypeSafeJevDecisionModel for a real Jev POC experiment.
