"""Evaluator registry used to constrain Jev's routing choices."""

from ai_eval.jev.models import EvaluatorSpec

EVALUATOR_REGISTRY: dict[str, EvaluatorSpec] = {
    "relevance": EvaluatorSpec(
        name="relevance",
        description="Checks whether the response addresses the user's request.",
        reason_to_run="Useful for general responses where answer quality matters.",
        required_signals=("input", "output"),
    ),
    "groundedness": EvaluatorSpec(
        name="groundedness",
        description="Checks whether the response is supported by supplied context.",
        reason_to_run="Required when retrieved/reference context is present.",
        required_signals=("input", "output", "context"),
    ),
    "pii": EvaluatorSpec(
        name="pii",
        description="Checks for personally identifiable information in input/output.",
        reason_to_run="Useful when user or application content may contain personal data.",
        required_signals=("input", "output"),
    ),
    "toxicity": EvaluatorSpec(
        name="toxicity",
        description="Checks for abusive, unsafe, or toxic content.",
        reason_to_run="Useful for safety-sensitive or user-generated content.",
        required_signals=("input", "output"),
    ),
    "tool_correctness": EvaluatorSpec(
        name="tool_correctness",
        description="Checks whether tool calls are appropriate and correctly used.",
        reason_to_run="Required when the agent invoked one or more tools.",
        required_signals=("input", "output", "tool_calls"),
    ),
}
