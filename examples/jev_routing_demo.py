"""Run the JEV intelligent evaluation-routing POC locally.

Usage:
    python examples/jev_routing_demo.py
"""

from ai_eval.jev.decision_engine import EvaluationDecisionEngine
from ai_eval.jev.mock import DemoJevDecisionModel
from ai_eval.jev.models import TraceSnapshot


TRACES = [
    TraceSnapshot(
        trace_id="demo-normal",
        input="What is the capital of France?",
        output="The capital of France is Paris.",
    ),
    TraceSnapshot(
        trace_id="demo-rag",
        input="According to the policy, what is the maximum batch size?",
        output="The maximum batch size is 500 units.",
        context=["Policy: Maximum batch size is 500 units."],
    ),
    TraceSnapshot(
        trace_id="demo-agent",
        input="Show me batches with yield below 90%.",
        output="There are 3 batches below the threshold.",
        tool_calls=[{"name": "query_batches", "arguments": {"yield_lt": 90}}],
    ),
    TraceSnapshot(
        trace_id="demo-pii",
        input="Send the report to user@example.com.",
        output="I can help prepare the report.",
    ),
]


def main() -> None:
    engine = EvaluationDecisionEngine(DemoJevDecisionModel())

    baseline = len(engine._registry)
    total_selected = 0

    print("\nJEV Intelligent Evaluation Routing POC")
    print("=" * 48)

    for trace in TRACES:
        plan = engine.plan(trace)
        total_selected += len(plan.selected)

        print(f"\nTrace: {trace.trace_id}")
        print(f"  Selected: {', '.join(plan.selected_names) or 'none'}")
        print(
            "  Skipped:  "
            + ", ".join(item.name for item in plan.skipped)
        )
        print(f"  Decision latency: {plan.decision_latency_ms:.2f} ms")

    baseline_calls = len(TRACES) * baseline
    jev_calls = total_selected
    reduction = 100 * (1 - jev_calls / baseline_calls)

    print("\nBenchmark")
    print("-" * 48)
    print(f"Baseline evaluator calls: {baseline_calls}")
    print(f"JEV-selected evaluator calls: {jev_calls}")
    print(f"Potential reduction: {reduction:.1f}%")
    print("\nNote: DemoJevDecisionModel is deterministic and local.")
    print("Swap it for TypeSafeJevDecisionModel for the real Jev POC.")


if __name__ == "__main__":
    main()
