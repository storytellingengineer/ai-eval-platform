from ai_eval.core.models import MetricResult
from ai_eval.jev.decision_engine import EvaluationDecisionEngine
from ai_eval.jev.executor import AdaptiveEvaluationPipeline
from ai_eval.jev.mock import DemoJevDecisionModel
from ai_eval.jev.models import TraceSnapshot


def _result(name: str) -> MetricResult:
    return MetricResult(metric_name=name, score=1.0, passed=True)


def test_pipeline_executes_only_selected_evaluators() -> None:
    calls: list[str] = []
    evaluators = {}

    for name in ("relevance", "groundedness", "tool_correctness"):
        evaluators[name] = lambda snapshot, name=name: (
            calls.append(name) or _result(name)
        )

    pipeline = AdaptiveEvaluationPipeline(
        EvaluationDecisionEngine(DemoJevDecisionModel()),
        evaluators,
    )

    result = pipeline.run(
        TraceSnapshot(
            trace_id="rag-1",
            input="What does the policy say?",
            output="500.",
            context=["Policy says 500."],
        )
    )

    assert result.executed_evaluators == ("relevance", "groundedness")
    assert calls == ["relevance", "groundedness"]
    assert result.evaluator_count == 2


def test_pipeline_fails_fast_for_missing_selected_evaluator() -> None:
    pipeline = AdaptiveEvaluationPipeline(
        EvaluationDecisionEngine(DemoJevDecisionModel()),
        {"relevance": lambda snapshot: _result("relevance")},
    )

    snapshot = TraceSnapshot(
        trace_id="tool-1",
        input="Find failed jobs.",
        output="Found 2.",
        tool_calls=[{"name": "search_jobs"}],
    )

    try:
        pipeline.run(snapshot)
    except KeyError as exc:
        assert "tool_correctness" in str(exc)
    else:
        raise AssertionError("Expected missing evaluator to raise KeyError")


def test_pipeline_rejects_mismatched_result_name() -> None:
    pipeline = AdaptiveEvaluationPipeline(
        EvaluationDecisionEngine(DemoJevDecisionModel()),
        {"relevance": lambda snapshot: _result("groundedness")},
    )

    try:
        pipeline.run(
            TraceSnapshot(trace_id="1", input="hello", output="hi")
        )
    except ValueError as exc:
        assert "metric_name" in str(exc)
    else:
        raise AssertionError("Expected mismatched result name to raise ValueError")
