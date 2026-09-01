"""Evaluation orchestration."""

from collections.abc import Iterable

from ai_eval.core.models import EvaluationResult, EvaluationSample
from ai_eval.metrics.base import Metric


class Evaluator:
    """Run a collection of metrics against an evaluation sample."""

    def __init__(self, metrics: Iterable[Metric]) -> None:
        self._metrics = tuple(metrics)
        if not self._metrics:
            raise ValueError("Evaluator requires at least one metric")

    def evaluate(self, sample: EvaluationSample) -> EvaluationResult:
        """Evaluate a single sample with every configured metric."""
        results = tuple(metric.evaluate(sample) for metric in self._metrics)
        return EvaluationResult(sample_id=sample.sample_id, metrics=results)

    def evaluate_many(
        self, samples: Iterable[EvaluationSample]
    ) -> list[EvaluationResult]:
        """Evaluate multiple samples in deterministic metric order."""
        return [self.evaluate(sample) for sample in samples]
