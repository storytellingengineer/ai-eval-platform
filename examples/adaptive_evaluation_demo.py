"""End-to-end local demo of risk-aware adaptive evaluation."""

from ai_eval.core.models import MetricResult
from ai_eval.jev.decision_engine import EvaluationDecisionEngine
from ai_eval.jev.executor import AdaptiveEvaluationPipeline
from ai_eval.jev.mock import DemoJevDecisionModel
from ai_eval.jev.models import TraceSnapshot


def make_demo_evaluator(name: str):
    def evaluate(snapshot: TraceSnapshot) -> MetricResult:
        # Replace these deterministic functions with real LLM judges/metrics.
        return MetricResult(
            metric_name=name,
            score=1.0,
            passed=True,
            explanation=f"Demo {name} evaluator executed.",
        )

    return evaluate


def main() -> None:
    evaluator_names = (
        "relevance",
        "groundedness",
        "pii",
        "toxicity",
        "tool_correctness",
    )
    pipeline = AdaptiveEvaluationPipeline(
        EvaluationDecisionEngine(DemoJevDecisionModel()),
        {name: make_demo_evaluator(name) for name in evaluator_names},
    )

    traces = [
        TraceSnapshot(
            trace_id="normal-1",
            input="What is the capital of France?",
            output="Paris.",
        ),
        TraceSnapshot(
            trace_id="rag-1",
            input="What does the policy say?",
            output="The policy says 500.",
            context=["Policy says 500."],
        ),
        TraceSnapshot(
            trace_id="agent-1",
            input="Find failed jobs.",
            output="Found 2.",
            tool_calls=[{"name": "search_jobs"}],
        ),
        TraceSnapshot(
            trace_id="pii-1",
            input="My email is user@example.com.",
            output="Thanks.",
        ),
    ]

    baseline_calls = len(traces) * len(evaluator_names)
    results = pipeline.run_many(traces)
    adaptive_calls = sum(result.evaluator_count for result in results)

    print(f"Baseline evaluator calls: {baseline_calls}")
    print(f"Adaptive evaluator calls: {adaptive_calls}")
    print(f"Calls avoided: {baseline_calls - adaptive_calls}")
    print()
    for result in results:
        print(
            result.trace_id,
            "->",
            list(result.executed_evaluators),
            f"(routing={result.plan.decision_latency_ms:.2f}ms)",
        )


if __name__ == "__main__":
    main()
