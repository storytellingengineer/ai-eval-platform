"""LLM-as-a-Judge implementation boundary.

The provider integration is intentionally deferred to a later milestone so
that the evaluation contracts can be tested independently of an external API.
"""

from collections.abc import Callable
from typing import Any

from ai_eval.core.models import EvaluationSample, MetricResult
from ai_eval.judges.base import Judge


class LLMJudge(Judge):
    """Judge adapter driven by an injected model callable."""

    name = "llm_judge"

    def __init__(self, model: Callable[[str], Any]) -> None:
        self._model = model

    def evaluate(self, sample: EvaluationSample) -> MetricResult:
        prompt = self._build_prompt(sample)
        response = self._model(prompt)
        raise NotImplementedError(
            "LLM judge response parsing will be implemented in the LLM evaluation milestone"
        )

    @staticmethod
    def _build_prompt(sample: EvaluationSample) -> str:
        return (
            "Evaluate the following AI response against the reference.\n\n"
            f"Input: {sample.input}\n"
            f"Output: {sample.output}\n"
            f"Reference: {sample.expected_output or '[none]'}\n"
        )
