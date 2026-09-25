"""Data contracts for dynamic evaluator selection."""

from dataclasses import dataclass, field
from typing import Any, Literal

EvaluatorName = Literal[
    "relevance",
    "groundedness",
    "pii",
    "toxicity",
    "tool_correctness",
]


@dataclass(frozen=True)
class TraceSnapshot:
    """Minimal Langfuse observation/trace state presented to the decision layer."""

    trace_id: str
    input: Any
    output: Any
    context: list[Any] = field(default_factory=list)
    tool_calls: list[dict[str, Any]] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class EvaluatorSpec:
    """Controlled evaluator registry entry."""

    name: EvaluatorName
    description: str
    reason_to_run: str
    required_signals: tuple[str, ...]


@dataclass(frozen=True)
class SelectedEvaluator:
    """One evaluator selected by Jev."""

    name: EvaluatorName
    confidence: float
    reason: str


@dataclass(frozen=True)
class EvaluationPlan:
    """Validated routing decision returned by the decision layer."""

    trace_id: str
    selected: tuple[SelectedEvaluator, ...]
    skipped: tuple[SelectedEvaluator, ...]
    model: str
    decision_latency_ms: float | None = None

    @property
    def selected_names(self) -> tuple[str, ...]:
        return tuple(item.name for item in self.selected)
