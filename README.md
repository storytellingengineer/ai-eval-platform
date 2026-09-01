# AI Eval Platform

> A production-oriented evaluation framework for LLM, RAG, and agentic AI systems.

[![CI](https://github.com/storytellingengineer/ai-eval-platform/actions/workflows/ci.yml/badge.svg)](https://github.com/storytellingengineer/ai-eval-platform/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

## Why this project?

Building an LLM application is only half the problem. The harder engineering problem is determining whether a change actually makes the system better.

AI Eval Platform is a practical evaluation layer for AI applications. It provides common abstractions for datasets, metrics, evaluation orchestration, structured results, aggregate reporting, and model-based judges. Future releases will add RAG evaluation, production observability integrations, experimentation, and CI/CD quality gates.

The project deliberately focuses on **measurement, reproducibility, regression detection, and engineering trade-offs** rather than another generic LLM wrapper.

## Current capabilities

### v0.1 — Evaluation foundation

- Immutable `EvaluationDataset` abstraction.
- Structured `EvaluationSample`, `MetricResult`, and `EvaluationResult` contracts.
- Pluggable `Metric` interface.
- Deterministic exact-match evaluation.
- Deterministic keyword-overlap baseline evaluation.
- `MetricRegistry` for named metric discovery.
- `Evaluator` for single and batch evaluation.
- `EvaluationReport` with mean scores and pass rates.
- Unit tests and GitHub Actions CI.

### v0.2 — LLM-as-a-Judge foundation

The current development milestone adds a provider-neutral judge architecture:

- `JudgeCriteria` and rubric configuration.
- Structured `JudgeResponse` and criterion-level scores.
- Rubric-driven judge prompts.
- Strict JSON response validation.
- Model-provider injection through a simple callable interface.
- Judge output normalized into the platform's existing `MetricResult` contract.
- Tests using a deterministic fake model, so the evaluation core does not require an API key.

The provider SDK integration is intentionally separate. This allows the same judge abstraction to work with different model providers later.

## Architecture

```text
                         AI Application
                               |
                               v
                     +-------------------+
                     | Evaluation Runner |
                     +---------+---------+
                               |
             +-----------------+------------------+
             |                 |                  |
             v                 v                  v
       Deterministic       LLM Judges        System Signals
          Metrics              |                  |
             |                 |                  |
             +-----------------+------------------+
                               |
                               v
                     Evaluation Results
                               |
                    +----------+----------+
                    |                     |
                    v                     v
              Experiment Store       CI/CD Gate
```

### LLM-as-a-Judge flow

```text
EvaluationSample
       |
       v
  JudgeConfig / Rubric
       |
       v
  Prompt Builder
       |
       v
   Model Provider
       |
       v
 Structured JSON
       |
       v
 Response Validator
       |
       v
   JudgeResponse
       |
       v
   MetricResult
```

## Design principles

1. **Provider independence** — evaluation logic should not be tightly coupled to one model provider.
2. **Metric composability** — individual metrics should be independently testable and replaceable.
3. **Structured results** — every evaluation should produce a consistent result object.
4. **Reproducibility** — datasets, configurations, model versions, and evaluation settings should eventually be recorded.
5. **Explicit failure** — invalid inputs and malformed judge responses should fail clearly rather than silently producing misleading results.
6. **Measurement before dashboards** — the evaluation engine must be trustworthy before a large platform layer is added.

## Evaluation dimensions

| Dimension | Examples | Status |
|---|---|---|
| Correctness | Exact match, reference comparison | **Implemented** |
| Relevance | Keyword overlap baseline | **Implemented** |
| LLM judgment | Rubric-based structured scoring | **Foundation implemented** |
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
│   ├── metrics/              # Deterministic metrics
│   ├── judges/
│   │   ├── base.py          # Judge interface
│   │   ├── schemas.py       # Rubric and judgment contracts
│   │   ├── prompts.py       # Rubric-driven prompt construction
│   │   ├── parser.py        # Strict response validation
│   │   └── llm_judge.py     # Provider-neutral judge adapter
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
python examples/llm_judge.py
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

- [x] Judge interface
- [x] Rubric configuration
- [x] Structured judge outputs
- [x] Strict response validation
- [x] Provider-neutral model adapter
- [ ] Production provider integrations
- [ ] Judge agreement analysis
- [ ] Calibration datasets
- [ ] Judge bias/variance experiments

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
- [ ] Provider-neutral observability adapter
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

**Stage: v0.2 — LLM-as-a-Judge foundation**

The judge architecture is now implemented without coupling the core to an external model provider. The next step is to add a real provider adapter and begin controlled judge-quality experiments.

## Contributing

Contributions, ideas, and critical discussion are welcome. Please open an issue before substantial changes so design decisions can be discussed openly.

## License

MIT License. See [LICENSE](LICENSE).
