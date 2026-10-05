"""Execute only the evaluators selected by the adaptive decision layer."""

from collections.abc import Callable, Iterable
from dataclasses import dataclass

from ai_eval.core.models import MetricResult
from ai_eval.jev.decision_engine import EvaluationDecisionEngine
from ai_eval.jev.models import EvaluationPlan, TraceSnapshot

EvaluatorFn = Callable[[TraceSnapshot], MetricResult]


@dataclass(frozen=True)
class AdaptiveEvaluationResult:
    """Evaluation output plus the routing decision that produced it."""

    trace_id: str
    plan: EvaluationPlan
    results: tuple[MetricResult, ...]

    @property
    def executed_evaluators(self) -> tuple[str, ...]:
        return tuple(result.metric_name for result in self.results)

    @property
    def evaluator_count(self) -> int:
        return len(self.results)


class AdaptiveEvaluationPipeline:
    """Route a trace, then execute only the selected evaluators."""

    def __init__(
        self,
        decision_engine: EvaluationDecisionEngine,
        evaluators: dict[str, EvaluatorFn],
    ) -> None:
        self._decision_engine = decision_engine
        self._evaluators = dict(evaluators)

    def run(self, snapshot: TraceSnapshot) -> AdaptiveEvaluationResult:
        """Create a plan and execute each selected evaluator exactly once."""
        plan = self._decision_engine.plan(snapshot)
        results: list[MetricResult] = []

        for selected in plan.selected:
            try:
                evaluator = self._evaluators[selected.name]
            except KeyError as exc:
                raise KeyError(
                    f"Evaluator '{selected.name}' is selected but has no implementation."
                ) from exc
            result = evaluator(snapshot)
            if result.metric_name != selected.name:
                raise ValueError(
                    f"Evaluator '{selected.name}' returned "
                    f"metric_name='{result.metric_name}'."
                )
            results.append(result)

        return AdaptiveEvaluationResult(
            trace_id=snapshot.trace_id,
            plan=plan,
            results=tuple(results),
        )

    def run_many(
        self, snapshots: Iterable[TraceSnapshot]
    ) -> list[AdaptiveEvaluationResult]:
        """Run adaptive evaluation over multiple traces."""
        return [self.run(snapshot) for snapshot in snapshots]
