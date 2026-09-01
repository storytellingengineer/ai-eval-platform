# AI Eval Platform

> A production-oriented evaluation framework for LLM, RAG, and agentic AI systems.

[![CI](https://github.com/storytellingengineer/ai-eval-platform/actions/workflows/ci.yml/badge.svg)](https://github.com/storytellingengineer/ai-eval-platform/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

## Why this project?

Building an LLM application is only half the problem. The harder engineering problem is determining whether a change actually makes the system better.

AI Eval Platform is a practical evaluation layer for AI applications. It provides common abstractions for datasets, metrics, evaluation orchestration, structured results, and aggregate reporting. Future releases will add model-based judges, RAG evaluation, production observability integrations, experimentation, and CI/CD quality gates.

The project deliberately focuses on **measurement, reproducibility, regression detection, and engineering trade-offs** rather than another generic LLM wrapper.

## Current capabilities — v0.1 foundation

The first working evaluation layer now includes:

- Immutable `EvaluationDataset` abstraction.
- Structured `EvaluationSample`, `MetricResult`, and `EvaluationResult` contracts.
- Pluggable `Metric` interface.
- Deterministic exact-match evaluation.
- Deterministic keyword-overlap baseline evaluation.
- `MetricRegistry` for named metric discovery.
- `Evaluator` for single and batch evaluation.
- `EvaluationReport` with mean scores and pass rates.
- Unit tests for core behavior.
- GitHub Actions CI for linting, type checking, and tests.

### Example

```python
from ai_eval.core import EvaluationDataset, EvaluationReport, EvaluationSample, Evaluator
from ai_eval.metrics import ExactMatchMetric, KeywordRelevanceMetric


dataset = EvaluationDataset.from_samples(
    "smoke-test",
    [
        EvaluationSample(
            sample_id="1",
            input="What is the capital of France?",
            output="Paris",
            expected_output="Paris",
        )
    ],
)

evaluator = Evaluator([ExactMatchMetric(), KeywordRelevanceMetric()])
results = evaluator.evaluate_many(dataset)
report = EvaluationReport.from_results(dataset.name, results)

for metric in report.metrics:
    print(metric.metric_name, metric.mean_score)
```

## Architecture

```text
                         AI Application
                               |
                               v
                     +-------------------+
                     | Evaluation Runner |
                     +---------+---------+
                               |
              +----------------+----------------+
              |                |                |
              v                v                v
        Deterministic      LLM Judges       System Signals
           Metrics                            
              |                |                |
              +----------------+----------------+
                               |
                               v
                     Evaluation Results
                               |
                    +----------+----------+
                    |                     |
                    v                     v
              Experiment Store       CI/CD Gate
```

The v0.1 implementation is intentionally smaller:

```text
Dataset
   |
   v
Evaluator
   |
   +----> Metrics
   |
   v
Evaluation Results
   |
   v
Aggregate Report
```

The production architecture will extend this core without coupling it to a specific model provider or observability vendor.

## Design principles

1. **Provider independence** — evaluation logic should not be tightly coupled to one model provider.
2. **Metric composability** — individual metrics should be independently testable and replaceable.
3. **Structured results** — every evaluation should produce a consistent result object.
4. **Reproducibility** — datasets, configurations, model versions, and evaluation settings should eventually be recorded.
5. **Explicit failure** — invalid inputs and unsupported evaluation states should fail clearly rather than silently producing misleading results.
6. **Measurement before dashboards** — the evaluation engine must be trustworthy before a large platform layer is added.

## Evaluation dimensions

| Dimension | Examples | Status |
|---|---|---|
| Correctness | Exact match, reference comparison | **Implemented** |
| Relevance | Keyword overlap baseline | **Implemented** |
| Faithfulness | Grounding against retrieved context | Planned |
| Retrieval | Recall@k, precision@k, ranking quality | Planned |
| Safety | Policy/guardrail checks | Planned |
| Agent quality | Tool selection, task completion | Planned |
| Performance | Latency, throughput | Planned |
| Cost | Tokens and estimated request cost | Planned |

## Project structure

```text
ai-eval-platform/
├── src/ai_eval/
│   ├── core/
│   │   ├── dataset.py       # Dataset abstraction
│   │   ├── evaluator.py     # Evaluation orchestration
│   │   ├── models.py        # Evaluation data contracts
│   │   ├── registry.py      # Metric registry
│   │   └── report.py        # Aggregate reporting
│   ├── metrics/              # Evaluation metrics
│   ├── judges/               # Model-based judges
│   └── pipelines/            # Evaluation workflows
├── tests/                    # Automated tests
├── examples/                 # Runnable examples
├── docs/                     # Architecture and methodology
├── .github/workflows/        # CI automation
├── pyproject.toml            # Project metadata and dependencies
└── README.md
```

## Quick start

### Requirements

- Python 3.11+
- Git
- A virtual environment is recommended

### Installation

```bash
git clone https://github.com/storytellingengineer/ai-eval-platform.git
cd ai-eval-platform
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -e ".[dev]"
```

### Run tests

```bash
pytest
```

### Run examples

```bash
python examples/basic_evaluation.py
python examples/evaluation_report.py
```

## Development philosophy

Each major capability should answer four questions:

1. **What are we measuring?**
2. **How reliable is the measurement?**
3. **What engineering decision does the measurement enable?**
4. **What are the failure modes and limitations?**

Evaluation numbers should never be presented without methodology and context.

## Roadmap

### Phase 1 — Evaluation foundation

- [x] Repository and project structure
- [x] Core evaluation data models
- [x] Dataset abstraction
- [x] Metric interface
- [x] Evaluator orchestration
- [x] Deterministic baseline metrics
- [x] Aggregate evaluation reports
- [x] Unit test suite
- [x] CI

### Phase 2 — LLM evaluation

- [ ] Provider abstraction
- [ ] LLM-as-a-Judge
- [ ] Judge prompt templates
- [ ] Structured judge outputs
- [ ] Judge agreement analysis
- [ ] Calibration datasets

### Phase 3 — RAG evaluation

- [ ] Retrieval metrics
- [ ] Faithfulness
- [ ] Context relevance
- [ ] Citation evaluation
- [ ] RAG regression datasets

### Phase 4 — Production evaluation

- [ ] Experiment tracking
- [ ] Latency and token metrics
- [ ] Cost tracking
- [ ] Evaluation reports with run metadata
- [ ] Regression detection
- [ ] CI/CD quality gates
- [ ] Observability adapter
- [ ] Langfuse integration

### Phase 5 — Agent evaluation

- [ ] Tool-call evaluation
- [ ] Trajectory evaluation
- [ ] Task completion metrics
- [ ] Failure categorization
- [ ] Human-in-the-loop evaluation

### Phase 6 — Platform layer

- [ ] REST API
- [ ] Persistent result storage
- [ ] Web dashboard
- [ ] Dataset management
- [ ] Experiment comparison

## Engineering questions this project explores

- When should an LLM judge be trusted?
- How do we calibrate an LLM judge against human judgments?
- How do different retrieval strategies affect downstream answer quality?
- How should evaluation datasets evolve without introducing leakage?
- How do we distinguish model regressions from evaluation noise?
- What quality threshold is appropriate for an automated deployment gate?
- How should quality, latency, and cost be optimized together?
- How can production traces become high-quality evaluation datasets?

## Current status

**Stage: v0.1 — Evaluation foundation**

The foundation is now implemented. The next milestone is **LLM-as-a-Judge**, followed by RAG evaluation and a provider-neutral observability layer. Langfuse is planned as an integration rather than a core dependency.

## Contributing

Contributions, ideas, and critical discussion are welcome. Please open an issue before substantial changes so design decisions can be discussed openly.

## License

MIT License. See [LICENSE](LICENSE).
