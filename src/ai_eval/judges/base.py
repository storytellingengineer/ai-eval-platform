"""Base interface for model-based judges."""

from abc import ABC, abstractmethod

from ai_eval.core.models import EvaluationSample, MetricResult


class Judge(ABC):
    """Contract for an evaluator powered by a model."""

    name: str

    @abstractmethod
    def evaluate(self, sample: EvaluationSample) -> MetricResult:
        """Evaluate a sample using a model-based judgment."""
        raise NotImplementedError
