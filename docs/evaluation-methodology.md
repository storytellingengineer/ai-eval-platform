# Evaluation Methodology

Evaluation results are only useful when the measurement itself is understood.

## Principles

### 1. Define the evaluation target

Every metric should clearly state whether it measures retrieval, generation, safety, agent behavior, or system performance.

### 2. Separate deterministic and model-based evaluation

Deterministic metrics are easier to reproduce. LLM judges can evaluate nuanced qualities but introduce model bias, variance, and calibration concerns.

### 3. Preserve evaluation context

A result should be traceable to its sample, metric, configuration, and eventually model/provider version.

### 4. Avoid single-metric decisions

A production decision should generally consider multiple dimensions such as quality, safety, latency, and cost.

### 5. Measure regressions, not just absolute scores

The platform should make it easy to compare a candidate system against a baseline using the same dataset and methodology.

## Planned judge methodology

For LLM-as-a-Judge, future versions will support:

- Explicit scoring rubrics.
- Structured judge outputs.
- Reference-aware and reference-free evaluation.
- Multiple judge runs for variance analysis.
- Human calibration datasets.
- Inter-rater agreement analysis.
- Judge-model comparison.

No model-based metric should be treated as ground truth without evidence of calibration.
