"""Langfuse integration helpers for the JEV routing POC."""

from typing import Any

from ai_eval.jev.models import EvaluationPlan


def push_decision_score(langfuse: Any, plan: EvaluationPlan) -> None:
    """Attach JEV's routing decision to the Langfuse trace as a text score."""
    selected = ", ".join(plan.selected_names) or "none"
    comment = (
        f"JEV model={plan.model}; selected={selected}; "
        f"decision_latency_ms={plan.decision_latency_ms:.2f}"
    )
    langfuse.create_score(
        name="jev_evaluation_plan",
        value=selected,
        trace_id=plan.trace_id,
        data_type="CATEGORICAL",
        comment=comment,
        metadata={
            "selected": list(plan.selected_names),
            "skipped": [item.name for item in plan.skipped],
            "model": plan.model,
            "decision_latency_ms": plan.decision_latency_ms,
        },
    )
