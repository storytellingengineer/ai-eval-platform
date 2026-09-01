"""Structured contracts for model-based judgments."""

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class JudgeCriteria:
    """A single criterion used by a judge rubric."""

    name: str
    description: str
    min_score: float = 0.0
    max_score: float = 1.0

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise ValueError("Criterion name cannot be empty")
        if self.min_score >= self.max_score:
            raise ValueError("Criterion min_score must be less than max_score")


@dataclass(frozen=True)
class JudgeConfig:
    """Configuration for one model-based judge."""

    name: str
    criteria: tuple[JudgeCriteria, ...]
    pass_threshold: float = 0.7
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise ValueError("Judge name cannot be empty")
        if not self.criteria:
            raise ValueError("Judge requires at least one criterion")
        if not 0.0 <= self.pass_threshold <= 1.0:
            raise ValueError("pass_threshold must be between 0 and 1")


@dataclass(frozen=True)
class JudgeScore:
    """Score assigned by a judge for one criterion."""

    criterion: str
    score: float
    explanation: str


@dataclass(frozen=True)
class JudgeResponse:
    """Normalized output expected from a model-based judge."""

    scores: tuple[JudgeScore, ...]
    overall_score: float
    passed: bool
    raw_response: str | None = None
