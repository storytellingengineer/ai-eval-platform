"""Decision engine that turns Jev answers into a safe evaluation plan."""

from time import perf_counter
from typing import Protocol

from ai_eval.jev.models import EvaluationPlan, SelectedEvaluator, TraceSnapshot
from ai_eval.jev.registry import EVALUATOR_REGISTRY


class DecisionModel(Protocol):
    """Minimal interface implemented by real Jev and the local demo adapter."""

    model_name: str

    def decide(self, state: dict, evaluator_registry: dict) -> dict:
        """Return a structured decision containing selected evaluator names."""


class EvaluationDecisionEngine:
    """Run a decision model and validate its output against a fixed registry."""

    def __init__(
        self,
        decision_model: DecisionModel,
        *,
        registry: dict = EVALUATOR_REGISTRY,
        min_confidence: float = 0.65,
    ) -> None:
        self._decision_model = decision_model
        self._registry = registry
        self._min_confidence = min_confidence

    def plan(self, snapshot: TraceSnapshot) -> EvaluationPlan:
        started = perf_counter()
        state = {
            "input": snapshot.input,
            "output": snapshot.output,
            "context": snapshot.context,
            "tool_calls": snapshot.tool_calls,
            "metadata": snapshot.metadata,
        }

        raw = self._decision_model.decide(state, self._registry)
        selected_raw = raw.get("selected", [])
        selected_names = set()

        selected: list[SelectedEvaluator] = []
        for item in selected_raw:
            name = str(item.get("name", ""))
            confidence = float(item.get("confidence", 0.0))
            if name not in self._registry:
                continue
            if confidence < self._min_confidence:
                continue
            if name in selected_names:
                continue

            selected_names.add(name)
            selected.append(
                SelectedEvaluator(
                    name=name,
                    confidence=max(0.0, min(1.0, confidence)),
                    reason=str(
                        item.get(
                            "reason",
                            self._registry[name].reason_to_run,
                        )
                    ),
                )
            )

        skipped = [
            SelectedEvaluator(
                name=name,
                confidence=1.0,
                reason="Not selected by the decision layer.",
            )
            for name in self._registry
            if name not in selected_names
        ]

        elapsed_ms = (perf_counter() - started) * 1000
        return EvaluationPlan(
            trace_id=snapshot.trace_id,
            selected=tuple(selected),
            skipped=tuple(skipped),
            model=self._decision_model.model_name,
            decision_latency_ms=elapsed_ms,
        )
