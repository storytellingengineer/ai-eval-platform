"""Real TypeSafe Jev adapter.

Install with:
    pip install typesafe-sdk

Set TYPESAFE_API_KEY before using this adapter.
"""

from typing import Any

from ai_eval.jev.models import EvaluatorSpec


class TypeSafeJevDecisionModel:
    """Use Jev to select which evaluators should run."""

    model_name = "jev-latest"

    def __init__(self, client: Any | None = None) -> None:
        if client is None:
            from typesafe_sdk import TypeSafeClient

            client = TypeSafeClient()
        self._client = client

    def decide(self, state: dict, evaluator_registry: dict[str, EvaluatorSpec]) -> dict:
        from typesafe_sdk import Choice

        criteria = {
            name: spec.description
            for name, spec in evaluator_registry.items()
        }

        question = Choice(
            instructions=(
                "Which evaluation dimensions are materially relevant to this "
                "LLM observation? Select every applicable dimension. "
                "Use the evaluator descriptions as the available choices."
            ),
            criteria=criteria,
            # Jev Choice is a single choice primitive. The POC therefore uses
            # a compact routing category and deterministic post-processing.
        )

        response = self._client.system_one(
            state=self._serialize_state(state),
            questions={"primary_dimension": question},
        )
        answer = response.answers["primary_dimension"]

        selected_name = getattr(answer, "choice", None)
        confidence = float(getattr(answer, "confidence", 0.0))
        if selected_name not in evaluator_registry:
            return {"selected": []}

        return {
            "selected": [
                {
                    "name": selected_name,
                    "confidence": confidence,
                    "reason": (
                        "Jev identified this evaluator as the primary relevant "
                        "evaluation dimension."
                    ),
                }
            ]
        }

    @staticmethod
    def _serialize_state(state: dict) -> str:
        import json

        return json.dumps(state, ensure_ascii=False, default=str)
