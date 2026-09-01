"""Deterministic correctness metrics."""

from ai_eval.core.models import EvaluationSample, MetricResult
from ai_eval.metrics.base import Metric


class ExactMatchMetric(Metric):
    """Score whether the generated output exactly matches the reference."""

    name = "exact_match"

    def evaluate(self, sample: EvaluationSample) -> MetricResult:
        if sample.expected_output is None:
            raise ValueError("ExactMatchMetric requires expected_output")

        score = float(sample.output.strip() == sample.expected_output.strip())
        return MetricResult(
            metric_name=self.name,
            score=score,
            passed=score == 1.0,
        )
