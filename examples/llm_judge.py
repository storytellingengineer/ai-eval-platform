"""Provider-neutral LLM-as-a-Judge example using a fake model."""

from ai_eval.core.models import EvaluationSample
from ai_eval.judges.llm_judge import LLMJudge
from ai_eval.judges.schemas import JudgeConfig, JudgeCriteria


config = JudgeConfig(
    name="answer-quality",
    criteria=(
        JudgeCriteria("correctness", "The answer is factually correct."),
        JudgeCriteria("relevance", "The answer directly addresses the question."),
    ),
    pass_threshold=0.7,
)

sample = EvaluationSample(
    sample_id="demo-001",
    input="What is the capital of France?",
    output="Paris is the capital of France.",
    expected_output="Paris",
)


def fake_model(_: str) -> str:
    """Stand-in for a real provider SDK call."""
    return '{"scores": [{"criterion": "correctness", "score": 1.0, "explanation": "Correct."}, {"criterion": "relevance", "score": 1.0, "explanation": "Directly answers the question."}], "overall_score": 1.0, "passed": true}'


result = LLMJudge(fake_model, config).evaluate(sample)
print(result)
