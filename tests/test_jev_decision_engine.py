from ai_eval.jev.decision_engine import EvaluationDecisionEngine
from ai_eval.jev.mock import DemoJevDecisionModel
from ai_eval.jev.models import TraceSnapshot


def test_normal_trace_selects_relevance_only() -> None:
    plan = EvaluationDecisionEngine(DemoJevDecisionModel()).plan(
        TraceSnapshot(
            trace_id="1",
            input="What is the capital of France?",
            output="Paris.",
        )
    )

    assert plan.selected_names == ("relevance",)
    assert "groundedness" in [item.name for item in plan.skipped]


def test_rag_trace_selects_groundedness() -> None:
    plan = EvaluationDecisionEngine(DemoJevDecisionModel()).plan(
        TraceSnapshot(
            trace_id="2",
            input="What does the policy say?",
            output="The policy says 500.",
            context=["Policy says 500."],
        )
    )

    assert "groundedness" in plan.selected_names


def test_tool_trace_selects_tool_correctness() -> None:
    plan = EvaluationDecisionEngine(DemoJevDecisionModel()).plan(
        TraceSnapshot(
            trace_id="3",
            input="Find failed jobs.",
            output="Found 2.",
            tool_calls=[{"name": "search_jobs"}],
        )
    )

    assert "tool_correctness" in plan.selected_names


def test_unknown_evaluator_is_rejected() -> None:
    class BadModel:
        model_name = "bad"

        def decide(self, state, evaluator_registry):
            return {
                "selected": [
                    {"name": "made_up_evaluator", "confidence": 1.0}
                ]
            }

    plan = EvaluationDecisionEngine(BadModel()).plan(
        TraceSnapshot(trace_id="4", input="hello", output="hi")
    )

    assert plan.selected_names == ()
