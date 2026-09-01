import pytest

from ai_eval.core.models import EvaluationSample
from ai_eval.judges.llm_judge import LLMJudge
from ai_eval.judges.parser import parse_judge_response
from ai_eval.judges.prompts import build_judge_prompt
from ai_eval.judges.schemas import JudgeConfig, JudgeCriteria


def config() -> JudgeConfig:
    return JudgeConfig(
        name="answer-quality",
        criteria=(
            JudgeCriteria("correctness", "The answer is factually correct."),
            JudgeCriteria("relevance", "The answer directly addresses the question."),
        ),
        pass_threshold=0.7,
    )


def sample() -> EvaluationSample:
    return EvaluationSample(
        sample_id="sample-001",
        input="What is the capital of France?",
        output="Paris is the capital of France.",
        expected_output="Paris",
    )


def test_prompt_contains_rubric_and_sample() -> None:
    prompt = build_judge_prompt(sample(), config())

    assert "correctness" in prompt
    assert "relevance" in prompt
    assert "Paris is the capital" in prompt
    assert '"overall_score"' in prompt


def test_parser_validates_structured_response() -> None:
    raw = '{"scores": [{"criterion": "correctness", "score": 1.0, "explanation": "Correct."}, {"criterion": "relevance", "score": 0.9, "explanation": "Direct."}], "overall_score": 0.95, "passed": true}'

    result = parse_judge_response(raw, config())

    assert result.overall_score == 0.95
    assert result.passed is True
    assert len(result.scores) == 2


def test_parser_rejects_unknown_criterion() -> None:
    raw = '{"scores": [{"criterion": "unknown", "score": 1.0, "explanation": "x"}], "overall_score": 1.0, "passed": true}'

    with pytest.raises(ValueError, match="Unknown judge criterion"):
        parse_judge_response(raw, config())


def test_llm_judge_normalizes_model_response() -> None:
    response = '{"scores": [{"criterion": "correctness", "score": 1.0, "explanation": "Correct."}, {"criterion": "relevance", "score": 1.0, "explanation": "Direct."}], "overall_score": 1.0, "passed": true}'
    judge = LLMJudge(lambda _: response, config())

    result = judge.evaluate(sample())

    assert result.metric_name == "llm_judge"
    assert result.score == 1.0
    assert result.passed is True
