"""Provider-neutral LLM-as-a-Judge implementation."""

from collections.abc import Callable
from typing import Any

from ai_eval.core.models import EvaluationSample, MetricResult
from ai_eval.judges.base import Judge
from ai_eval.judges.parser import parse_judge_response
from ai_eval.judges.prompts import build_judge_prompt
from ai_eval.judges.schemas import JudgeConfig


class LLMJudge(Judge):
    """Judge adapter driven by an injected model callable."""

    name = "llm_judge"

    def __init__(self, model: Callable[[str], Any], config: JudgeConfig) -> None:
        self._model = model
        self._config = config

    def evaluate(self, sample: EvaluationSample) -> MetricResult:
        """Run the model and normalize its structured judgment."""
        prompt = build_judge_prompt(sample, self._config)
        raw_response = self._model(prompt)
        if not isinstance(raw_response, str):
            raise TypeError("Judge model callable must return a string")

        judgment = parse_judge_response(raw_response, self._config)
        explanation = "; ".join(
            f"{score.criterion}: {score.explanation}" for score in judgment.scores
        )

        return MetricResult(
            metric_name=self.name,
            score=judgment.overall_score,
            passed=judgment.passed,
            explanation=explanation,
            metadata={
                "judge": self._config.name,
                "criteria": [score.criterion for score in judgment.scores],
            },
        )
