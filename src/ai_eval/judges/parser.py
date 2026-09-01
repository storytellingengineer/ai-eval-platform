"""Parsing and validation for structured judge responses."""

import json
from typing import Any

from ai_eval.judges.schemas import JudgeConfig, JudgeResponse, JudgeScore


def parse_judge_response(
    raw_response: str, config: JudgeConfig
) -> JudgeResponse:
    """Parse and validate a JSON judge response against its rubric."""
    try:
        payload: Any = json.loads(raw_response)
    except json.JSONDecodeError as exc:
        raise ValueError("Judge response is not valid JSON") from exc

    if not isinstance(payload, dict):
        raise ValueError("Judge response must be a JSON object")

    raw_scores = payload.get("scores")
    if not isinstance(raw_scores, list):
        raise ValueError("Judge response must contain a scores array")

    criteria = {criterion.name: criterion for criterion in config.criteria}
    scores: list[JudgeScore] = []

    for item in raw_scores:
        if not isinstance(item, dict):
            raise ValueError("Each judge score must be an object")

        name = item.get("criterion")
        score = item.get("score")
        explanation = item.get("explanation")

        if name not in criteria:
            raise ValueError(f"Unknown judge criterion: {name}")
        if not isinstance(score, (int, float)) or isinstance(score, bool):
            raise ValueError(f"Invalid score for criterion: {name}")
        if not isinstance(explanation, str):
            raise ValueError(f"Missing explanation for criterion: {name}")

        criterion = criteria[name]
        if not criterion.min_score <= score <= criterion.max_score:
            raise ValueError(f"Score outside allowed range for criterion: {name}")

        scores.append(
            JudgeScore(criterion=name, score=float(score), explanation=explanation)
        )

    if {score.criterion for score in scores} != set(criteria):
        raise ValueError("Judge response must score every configured criterion")

    overall = payload.get("overall_score")
    passed = payload.get("passed")
    if not isinstance(overall, (int, float)) or isinstance(overall, bool):
        raise ValueError("overall_score must be numeric")
    if not isinstance(passed, bool):
        raise ValueError("passed must be boolean")
    if not 0.0 <= float(overall) <= 1.0:
        raise ValueError("overall_score must be between 0 and 1")

    return JudgeResponse(
        scores=tuple(scores),
        overall_score=float(overall),
        passed=passed,
        raw_response=raw_response,
    )
