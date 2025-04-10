# metrics/metrics.py
from ragas import SingleTurnSample
from ragas.metrics import (
    ContextEntitiesRecall,
    ContextPrecision,
    ContextRecall,
    Faithfulness,
    NoiseSensitivity
)

class RAGMetricsEvaluator:
    def __init__(self, evaluator_llm):
        self.evaluator_llm = evaluator_llm
        self.context_entities_recall = ContextEntitiesRecall()
        self.context_precision = ContextPrecision()
        self.context_recall = ContextRecall()
        self.faithfulness = Faithfulness()
        self.noise_sensitivity = NoiseSensitivity()

    def compute_context_entities_recall(self, user_input, retrieved_contexts, reference_entities):
        sample = SingleTurnSample(
            user_input=user_input,
            retrieved_contexts=retrieved_contexts,
            reference_entities=reference_entities
        )
        return self.context_entities_recall.single_turn_ascore(sample)

    def compute_context_precision(self, user_input, retrieved_contexts, reference_contexts):
        sample = SingleTurnSample(
            user_input=user_input,
            retrieved_contexts=retrieved_contexts,
            reference_contexts=reference_contexts
        )
        return self.context_precision.single_turn_ascore(sample)

    def compute_context_recall(self, user_input, retrieved_contexts, reference_contexts):
        sample = SingleTurnSample(
            user_input=user_input,
            retrieved_contexts=retrieved_contexts,
            reference_contexts=reference_contexts
        )
        return self.context_recall.single_turn_ascore(sample)

    def compute_faithfulness(self, user_input, generated_text, retrieved_contexts):
        sample = SingleTurnSample(
            user_input=user_input,
            response=generated_text,
            retrieved_contexts=retrieved_contexts
        )
        return self.faithfulness.single_turn_ascore(sample)

    def compute_noise_sensitivity(self, user_input, retrieved_contexts, noisy_contexts, reference_contexts):
        sample = SingleTurnSample(
            user_input=user_input,
            retrieved_contexts=noisy_contexts,
            reference_contexts=reference_contexts
        )
        return self.noise_sensitivity.single_turn_ascore(sample)
