# AI Eval Platform

> A production-oriented evaluation framework for LLM, RAG, and agentic AI systems.

[![CI](https://github.com/storytellingengineer/ai-eval-platform/actions/workflows/ci.yml/badge.svg)](https://github.com/storytellingengineer/ai-eval-platform/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

## Why this project?

Building an LLM application is only half the problem. The harder engineering problem is determining whether a change actually makes the system better.

AI Eval Platform is being built as a practical evaluation layer for AI applications. It provides a common interface for running evaluation datasets, computing deterministic metrics, invoking model-based judges, comparing experiments, and eventually enforcing quality gates in CI/CD.

The project deliberately focuses on **measurement, reproducibility, regression detection, and engineering trade-offs** rather than another generic LLM wrapper.

## Goals

- Provide a clean, extensible evaluation API.
- Support LLM, RAG, and agent evaluation workflows.
- Separate evaluation orchestration from individual metrics and judges.
- Make evaluation results structured, reproducible, and machine-readable.
- Support both deterministic metrics and LLM-as-a-Judge evaluation.
- Make quality regressions visible before production deployment.
- Track quality, latency, token usage, and cost as first-class signals.
- Evolve toward a CI/CD quality gate for AI systems.

## Non-goals

This project is not intended to be:

- A model-training framework.
- A replacement for vector databases or LLM providers.
- A single vendor-specific evaluation SDK.
- A dashboard-first product before the evaluation core is reliable.

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

The core design follows a few principles:

1. **Provider independence** — evaluation logic should not be tightly coupled to one model provider.
2. **Metric composability** — individual metrics should be independently testable and replaceable.
3. **Structured results** — every evaluation should produce a consistent result object.
4. **Reproducibility** — datasets, configurations, model versions, and evaluation settings should be recorded.
5. **Fail explicitly** — missing inputs, invalid configurations, and judge failures should be observable rather than silently ignored.

## Evaluation dimensions

The roadmap covers several classes of evaluation:

| Dimension | Examples | Status |
|---|---|---|
| Correctness | Exact match, reference comparison | Planned |
| Relevance | Answer/query relevance | Planned |
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
│   ├── core/             # Core evaluation contracts and orchestration
│   ├── metrics/          # Evaluation metrics
│   ├── judges/           # Model-based judges
│   └── pipelines/        # Evaluation workflows
├── tests/                # Automated tests
├── examples/             # Small runnable examples
├── docs/                  # Architecture and methodology documentation
├── .github/workflows/    # CI automation
├── pyproject.toml        # Project metadata and dependencies
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

### Run the example

```bash
python examples/basic_evaluation.py
```

## Development philosophy

This repository is intentionally being developed incrementally.

Each major capability should answer four questions:

1. **What are we measuring?**
2. **How reliable is the measurement?**
3. **What engineering decision does the measurement enable?**
4. **What are the failure modes and limitations?**

That means evaluation numbers should never be presented without methodology and context.

## Roadmap

### Phase 1 — Evaluation foundation

- [x] Repository and project structure
- [ ] Core evaluation data models
- [ ] Metric interface
- [ ] Evaluator orchestration
- [ ] Deterministic correctness/relevance metrics
- [ ] Unit test suite

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
- [ ] Evaluation reports
- [ ] Regression detection
- [ ] CI/CD quality gates

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

## Current status

**Stage: Foundation / v0.1 development**

The initial release establishes the architecture and contracts. Functionality will be added through small, testable increments rather than a large monolithic implementation.

## Contributing

Contributions, ideas, and critical discussion are welcome. Please open an issue before substantial changes so design decisions can be discussed openly.

## License

MIT License. See [LICENSE](LICENSE).
