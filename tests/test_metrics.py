from ai_eval.core.models import EvaluationSample
from ai_eval.metrics import ExactMatchMetric, KeywordRelevanceMetric


def test_exact_match_passes_for_matching_reference() -> None:
    sample = EvaluationSample(
        sample_id="1",
        input="What is 2 + 2?",
        output="4",
        expected_output="4",
    )

    result = ExactMatchMetric().evaluate(sample)

    assert result.score == 1.0
    assert result.passed is True


def test_exact_match_fails_for_different_output() -> None:
    sample = EvaluationSample(
        sample_id="1",
        input="What is 2 + 2?",
        output="5",
        expected_output="4",
    )

    result = ExactMatchMetric().evaluate(sample)

    assert result.score == 0.0
    assert result.passed is False


def test_keyword_relevance_measures_reference_overlap() -> None:
    sample = EvaluationSample(
        sample_id="1",
        input="Explain Python",
        output="Python is a programming language",
        expected_output="Python programming language",
    )

    result = KeywordRelevanceMetric().evaluate(sample)

    assert result.score == 1.0
