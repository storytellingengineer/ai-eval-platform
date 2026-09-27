"""Deterministic local decision model for demos and tests."""

from typing import Any


class DemoJevDecisionModel:
    """A local Jev-shaped router so the POC runs without an API key.

    This intentionally mirrors the structured contract of the real Jev adapter.
    It is not presented as a substitute for Jev's model quality.
    """

    model_name = "jev-demo-heuristic"

    def decide(self, state: dict, evaluator_registry: dict) -> dict:
        text = f"{state.get('input', '')} {state.get('output', '')}".lower()
        context = state.get("context") or []
        tools = state.get("tool_calls") or []

        selected: list[dict[str, Any]] = [
            {
                "name": "relevance",
                "confidence": 0.96,
                "reason": "Every application response should be checked for relevance.",
            }
        ]

        if context:
            selected.append(
                {
                    "name": "groundedness",
                    "confidence": 0.98,
                    "reason": "Reference/retrieved context is present.",
                }
            )

        if tools:
            selected.append(
                {
                    "name": "tool_correctness",
                    "confidence": 0.99,
                    "reason": "The observation contains tool calls.",
                }
            )

        pii_markers = ("email", "phone", "address", "passport", "aadhaar", "ssn")
        if any(marker in text for marker in pii_markers):
            selected.append(
                {
                    "name": "pii",
                    "confidence": 0.94,
                    "reason": "The content contains a possible PII indicator.",
                }
            )

        safety_markers = ("kill", "bomb", "hack", "abuse", "threat")
        if any(marker in text for marker in safety_markers):
            selected.append(
                {
                    "name": "toxicity",
                    "confidence": 0.91,
                    "reason": "The content contains a safety-sensitive indicator.",
                }
            )

        return {"selected": selected}
