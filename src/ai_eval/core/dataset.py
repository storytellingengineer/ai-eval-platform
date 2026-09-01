"""Dataset abstraction for repeatable evaluation runs."""

from collections.abc import Iterable, Iterator
from dataclasses import dataclass

from ai_eval.core.models import EvaluationSample


@dataclass(frozen=True)
class EvaluationDataset:
    """Named collection of evaluation samples.

    A dataset is immutable at runtime so an evaluation run can be associated
    with a stable set of samples.
    """

    name: str
    samples: tuple[EvaluationSample, ...]

    @classmethod
    def from_samples(
        cls, name: str, samples: Iterable[EvaluationSample]
    ) -> "EvaluationDataset":
        materialized = tuple(samples)
        if not name.strip():
            raise ValueError("Dataset name cannot be empty")
        if not materialized:
            raise ValueError("Dataset requires at least one sample")
        return cls(name=name, samples=materialized)

    def __iter__(self) -> Iterator[EvaluationSample]:
        return iter(self.samples)

    def __len__(self) -> int:
        return len(self.samples)
