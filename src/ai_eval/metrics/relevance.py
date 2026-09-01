"""Simple deterministic relevance metric used for the foundation release."""

from ai_eval.core.models import EvaluationSample, MetricResult
from ai_eval.metrics.base import Metric


class KeywordRelevanceMetric(Metric):
    """Measure overlap between expected and generated output tokens.

    This is intentionally simple and deterministic. It is a baseline metric,
    not a semantic relevance evaluator.
    """

    name = "keyword_relevance"

    def evaluate(self, sample: EvaluationSample) -> MetricResult:
        if sample.expected_output is None:
            raise ValueError("KeywordRelevanceMetric requires expected_output")

        expected = set(sample.expected_output.lower().split())
        output = set(sample.output.lower().split())
        if not expected:
            score = 1.0 if not output else 0.0
        else:
            score = len(expected & output) / len(expected)

        return MetricResult(metric_name=self.name, score=score)
