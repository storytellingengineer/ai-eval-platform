"""Base interface for evaluation metrics."""

from abc import ABC, abstractmethod

from ai_eval.core.models import EvaluationSample, MetricResult


class Metric(ABC):
    """Contract implemented by all evaluation metrics."""

    name: str

    @abstractmethod
    def evaluate(self, sample: EvaluationSample) -> MetricResult:
        """Evaluate one sample and return a structured metric result."""
        raise NotImplementedError
