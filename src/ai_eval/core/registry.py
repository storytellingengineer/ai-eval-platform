"""Registry for discovering configured evaluation metrics."""

from collections.abc import Iterable

from ai_eval.metrics.base import Metric


class MetricRegistry:
    """Named registry of metric implementations."""

    def __init__(self, metrics: Iterable[Metric] = ()) -> None:
        self._metrics: dict[str, Metric] = {}
        for metric in metrics:
            self.register(metric)

    def register(self, metric: Metric) -> None:
        """Register a metric by its unique name."""
        if not metric.name.strip():
            raise ValueError("Metric name cannot be empty")
        if metric.name in self._metrics:
            raise ValueError(f"Metric already registered: {metric.name}")
        self._metrics[metric.name] = metric

    def get(self, name: str) -> Metric:
        """Return a registered metric or raise a clear error."""
        try:
            return self._metrics[name]
        except KeyError as exc:
            raise KeyError(f"Unknown metric: {name}") from exc

    def all(self) -> tuple[Metric, ...]:
        """Return metrics in registration order."""
        return tuple(self._metrics.values())
