"""Aggregation of sample-level evaluation results."""

from dataclasses import dataclass

from ai_eval.core.models import EvaluationResult


@dataclass(frozen=True)
class MetricSummary:
    """Aggregate statistics for one metric."""

    metric_name: str
    sample_count: int
    mean_score: float
    pass_rate: float | None


@dataclass(frozen=True)
class EvaluationReport:
    """Aggregate report for an evaluation run."""

    dataset_name: str
    sample_count: int
    metrics: tuple[MetricSummary, ...]

    @classmethod
    def from_results(
        cls, dataset_name: str, results: list[EvaluationResult]
    ) -> "EvaluationReport":
        if not results:
            raise ValueError("Cannot create a report from zero results")

        metric_values: dict[str, list[float]] = {}
        metric_passes: dict[str, list[bool]] = {}

        for result in results:
            for metric in result.metrics:
                metric_values.setdefault(metric.metric_name, []).append(metric.score)
                if metric.passed is not None:
                    metric_passes.setdefault(metric.metric_name, []).append(metric.passed)

        summaries = []
        for name, scores in metric_values.items():
            passes = metric_passes.get(name)
            summaries.append(
                MetricSummary(
                    metric_name=name,
                    sample_count=len(scores),
                    mean_score=sum(scores) / len(scores),
                    pass_rate=(sum(passes) / len(passes)) if passes else None,
                )
            )

        return cls(
            dataset_name=dataset_name,
            sample_count=len(results),
            metrics=tuple(summaries),
        )
