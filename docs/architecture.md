# Architecture

## Design intent

The platform is organized around four replaceable layers:

```text
Dataset / Samples
       |
       v
Evaluation Pipeline
       |
       v
    Evaluator
       |
  +----+----------------+
  |                     |
  v                     v
Metrics               Judges
  |                     |
  +----------+----------+
             |
             v
     Structured Results
```

### Core

`EvaluationSample`, `MetricResult`, and `EvaluationResult` define the stable data contracts.

### Metrics

Metrics implement a common interface and are independently testable. Deterministic metrics do not require an external model provider.

### Judges

Judges are model-powered evaluators. The interface is isolated from provider-specific clients so provider integrations can evolve without changing the core evaluation model.

### Pipelines

Pipelines compose metrics and judges into repeatable workflows.

## Why this separation?

A useful evaluation framework should not make the evaluation engine depend on a specific model, vendor, or dashboard. The core should remain small while integrations can grow around it.

## Future production architecture

The eventual platform will add dataset storage, asynchronous execution, experiment tracking, observability, API access, and CI/CD quality gates. Those concerns are deliberately not mixed into the foundation release.
