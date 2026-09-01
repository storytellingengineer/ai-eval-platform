"""High-level evaluation pipeline."""

from collections.abc import Iterable

from ai_eval.core.evaluator import Evaluator
from ai_eval.core.models import EvaluationResult, EvaluationSample
from ai_eval.metrics.base import Metric


class EvaluationPipeline:
    """Small orchestration layer around the core evaluator."""

    def __init__(self, metrics: Iterable[Metric]) -> None:
        self.evaluator = Evaluator(metrics)

    def run(self, samples: Iterable[EvaluationSample]) -> list[EvaluationResult]:
        """Run configured evaluation metrics over a dataset."""
        return self.evaluator.evaluate_many(samples)
