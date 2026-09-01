"""Run a dataset and print its aggregate evaluation report."""

from ai_eval.core import EvaluationDataset, EvaluationReport, EvaluationSample, Evaluator
from ai_eval.metrics import ExactMatchMetric, KeywordRelevanceMetric


dataset = EvaluationDataset.from_samples(
    "foundation-smoke-test",
    [
        EvaluationSample(
            sample_id="capital-france",
            input="What is the capital of France?",
            output="Paris",
            expected_output="Paris",
        ),
        EvaluationSample(
            sample_id="capital-uk",
            input="What is the capital of the United Kingdom?",
            output="London",
            expected_output="Paris",
        ),
    ],
)

evaluator = Evaluator([ExactMatchMetric(), KeywordRelevanceMetric()])
results = evaluator.evaluate_many(dataset)
report = EvaluationReport.from_results(dataset.name, results)

print(f"Dataset: {report.dataset_name}")
print(f"Samples: {report.sample_count}")
for metric in report.metrics:
    pass_rate = "n/a" if metric.pass_rate is None else f"{metric.pass_rate:.2%}"
    print(
        f"{metric.metric_name}: mean={metric.mean_score:.2f}, "
        f"pass_rate={pass_rate}"
    )
