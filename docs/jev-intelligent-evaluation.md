# JEV + Langfuse Intelligent Evaluation

## Hypothesis

Running every evaluator on every production observation is often unnecessary. A lightweight decision layer can inspect the observation and select only the evaluation dimensions that are relevant.

This POC uses **TypeSafe's Jev** as that decision layer.

## Architecture

```
Application / Agent
       |
       v
   Langfuse
       |
       | observation state
       v
+----------------------+
| JEV Decision Layer   |
| "What should we eval?"|
+----------+-----------+
           |
     Evaluation Plan
           |
    +------+------+------+
    |      |      |      |
    v      v      v      v
 Relevance RAG    PII  Tool-use ...
    |      |      |      |
    +------+------+------+
           |
           v
      Evaluation Scores
           |
           v
        Langfuse
```

## Important distinction

Jev is not replacing the downstream evaluator.

- **Jev:** decides which evaluation dimensions are relevant.
- **Evaluator:** performs the actual quality/safety/groundedness judgment.
- **Langfuse:** stores traces and scores.

The current POC keeps the evaluator registry under application control so Jev cannot invent evaluator names.

## Why this is interesting

Langfuse now supports Jev directly as a decision-model evaluator. Jev is designed for typed decisions, returns probabilities/confidence, and can answer multiple typed questions in one call. This POC explores a different orchestration pattern: use Jev *before* expensive/open-ended evaluators to dynamically route evaluation work.

The POC should be measured against a baseline:

```
Baseline:
N traces × M evaluators

JEV:
N traces × selected evaluators
```

Primary metrics:

- evaluator execution reduction
- latency added by routing
- cost reduction
- evaluator coverage / missed-issue rate
- false selection rate

Do not claim cost or quality improvements until measured.

## Real Jev integration

Install:

```bash
pip install typesafe-sdk
export TYPESAFE_API_KEY="..."
```

Then replace:

```python
from ai_eval.jev.mock import DemoJevDecisionModel
```

with:

```python
from ai_eval.jev.typesafe_client import TypeSafeJevDecisionModel

engine = EvaluationDecisionEngine(TypeSafeJevDecisionModel())
```

The TypeSafe API accepts a state and typed questions at `POST https://api.typesafe.ai/v1/systemone`. The Python SDK exposes `Choice`, `Score`, and `Noul` primitives.

## Langfuse score

Once a real Langfuse trace exists, the routing plan can be written back as a score:

```python
from langfuse import get_client
from ai_eval.jev.langfuse import push_decision_score

langfuse = get_client()
push_decision_score(langfuse, plan)
```

## Next POC iteration

1. Replace the demo router with real Jev.
2. Add actual Langfuse observation retrieval.
3. Execute 5 downstream evaluators conditionally.
4. Push downstream scores back to Langfuse.
5. Run 20–50 synthetic traces.
6. Compare all-evaluators vs JEV-routed evaluation.
