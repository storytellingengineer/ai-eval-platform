"""Data contracts used by the evaluation engine."""

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class EvaluationSample:
    """One input/output example presented to an evaluator."""

    sample_id: str
    input: str
    output: str
    expected_output: str | None = None
    context: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class MetricResult:
    """Result returned by an individual metric."""

    metric_name: str
    score: float
    passed: bool | None = None
    explanation: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class EvaluationResult:
    """Aggregate result for one evaluated sample."""

    sample_id: str
    metrics: tuple[MetricResult, ...]
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def scores(self) -> dict[str, float]:
        """Return metric names mapped to their scores."""
        return {metric.metric_name: metric.score for metric in self.metrics}
