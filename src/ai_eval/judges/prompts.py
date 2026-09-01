"""Prompt construction for LLM-as-a-Judge."""

from ai_eval.core.models import EvaluationSample
from ai_eval.judges.schemas import JudgeConfig


def build_judge_prompt(sample: EvaluationSample, config: JudgeConfig) -> str:
    """Build a provider-neutral evaluation prompt from a rubric."""
    criteria = "\n".join(
        f"- {criterion.name}: {criterion.description} "
        f"(score {criterion.min_score} to {criterion.max_score})"
        for criterion in config.criteria
    )

    return f"""You are an evaluation judge. Evaluate the candidate answer using only the rubric provided.

Return a JSON object with this shape:
{{
  "scores": [
    {{"criterion": "criterion name", "score": 0.0, "explanation": "brief evidence-based explanation"}}
  ],
  "overall_score": 0.0,
  "passed": false
}}

RUBRIC:
{criteria}

INPUT:
{sample.input}

CANDIDATE ANSWER:
{sample.output}

REFERENCE ANSWER:
{sample.expected_output or "[No reference answer provided]"}

Do not add markdown fences. Keep explanations concise and grounded in the provided evidence.
"""
