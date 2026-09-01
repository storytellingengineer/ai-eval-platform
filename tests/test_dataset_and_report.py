from ai_eval.core import EvaluationDataset, EvaluationReport, EvaluationSample
from ai_eval.metrics import ExactMatchMetric, KeywordRelevanceMetric
from ai_eval.core.evaluator import Evaluator


def sample(sample_id: str, output: str, expected: str) -> EvaluationSample:
    return EvaluationSample(
        sample_id=sample_id,
        input="question",
        output=output,
        expected_output=expected,
    )


def test_dataset_is_immutable_and_iterable() -> None:
    dataset = EvaluationDataset.from_samples(
        "smoke",
        [sample("1", "Paris", "Paris")],
    )

    assert len(dataset) == 1
    assert [item.sample_id for item in dataset] == ["1"]


def test_report_aggregates_metric_scores_and_pass_rate() -> None:
    dataset = EvaluationDataset.from_samples(
        "smoke",
        [sample("1", "Paris", "Paris"), sample("2", "London", "Paris")],
    )
    evaluator = Evaluator([ExactMatchMetric(), KeywordRelevanceMetric()])
    results = evaluator.evaluate_many(dataset)

    report = EvaluationReport.from_results(dataset.name, results)
    summaries = {metric.metric_name: metric for metric in report.metrics}

    assert report.sample_count == 2
    assert summaries["exact_match"].mean_score == 0.5
    assert summaries["exact_match"].pass_rate == 0.5
