"""Real TypeSafe Jev adapter.

Install with:
    pip install typesafe-sdk

Set TYPESAFE_API_KEY before using this adapter.
"""

from typing import Any

from ai_eval.jev.models import EvaluatorSpec


class TypeSafeJevDecisionModel:
    """Use Jev's atomic Noul questions to route evaluation dimensions."""

    model_name = "jev-latest"

    def __init__(self, client: Any | None = None) -> None:
        if client is None:
            from typesafe_sdk import TypeSafeClient

            client = TypeSafeClient()
        self._client = client

    def decide(self, state: dict, evaluator_registry: dict[str, EvaluatorSpec]) -> dict:
        from typesafe_sdk import Noul

        questions = {
            name: Noul(
                instructions=(
                    f"Should the '{name}' evaluator run on this observation? "
                    f"Evaluator purpose: {spec.description} "
                    f"Run it only when the observation contains evidence that "
                    f"this evaluation dimension is relevant."
                )
            )
            for name, spec in evaluator_registry.items()
        }

        response = self._client.system_one(
            state=self._serialize_state(state),
            questions=questions,
        )

        selected = []
        for name in evaluator_registry:
            answer = response.answers[name]
            probability = float(getattr(answer, "noul", 0.0))
            selected.append(
                {
                    "name": name,
                    "confidence": probability,
                    "reason": (
                        f"Jev P(relevant)={probability:.2f} for {name}."
                    ),
                }
            )

        return {"selected": selected}

    @staticmethod
    def _serialize_state(state: dict) -> str:
        import json

        return json.dumps(state, ensure_ascii=False, default=str)
