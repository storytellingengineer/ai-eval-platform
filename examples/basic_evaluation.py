"""Minimal example of the evaluation foundation."""

from ai_eval.core.models import EvaluationSample
from ai_eval.metrics import ExactMatchMetric, KeywordRelevanceMetric
from ai_eval.pipelines.evaluation import EvaluationPipeline


samples = [
    EvaluationSample(
        sample_id="capital-france",
        input="What is the capital of France?",
        output="Paris",
        expected_output="Paris",
    ),
    EvaluationSample(
        sample_id="python",
        input="What is Python?",
        output="Python is a programming language.",
        expected_output="Python programming language",
    ),
]

pipeline = EvaluationPipeline([ExactMatchMetric(), KeywordRelevanceMetric()])

for result in pipeline.run(samples):
    print(result.sample_id)
    for metric_name, score in result.scores.items():
        print(f"  {metric_name}: {score:.2f}")
