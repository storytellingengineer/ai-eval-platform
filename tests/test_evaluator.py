import pytest

from ai_eval.core.evaluator import Evaluator
from ai_eval.core.models import EvaluationSample
from ai_eval.metrics import ExactMatchMetric


def test_evaluator_returns_structured_results() -> None:
    evaluator = Evaluator([ExactMatchMetric()])
    sample = EvaluationSample(
        sample_id="sample-001",
        input="What is the capital of France?",
        output="Paris",
        expected_output="Paris",
    )

    result = evaluator.evaluate(sample)

    assert result.sample_id == "sample-001"
    assert result.scores == {"exact_match": 1.0}


def test_evaluator_rejects_empty_metric_collection() -> None:
    with pytest.raises(ValueError, match="at least one metric"):
        Evaluator([])
