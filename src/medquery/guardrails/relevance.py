from medquery.guardrails.result import GuardrailResult
from medquery.schemas.retrieval import RetrievalResult


class RelevanceGuardrail:
    def __init__(
        self,
        min_top_score: float = 0.30,
        min_top3_average: float = 0.25,
    ) -> None:
        self.min_top_score = min_top_score
        self.min_top3_average = min_top3_average

    def check(
        self,
        results: list[RetrievalResult],
    ) -> GuardrailResult:
        if not results:
            return GuardrailResult(
                allowed=False,
                reason="No relevant documents were retrieved.",
            )

        top_score = results[0].dense_score

        top_3_results = results[:3]

        top_3_average = sum(
            result.dense_score
            for result in top_3_results
        ) / len(top_3_results)

        if (
            top_score >= self.min_top_score
            and top_3_average >= self.min_top3_average
        ):
            return GuardrailResult(
                allowed=True,
                reason="Sufficient retrieval evidence found.",
            )

        return GuardrailResult(
            allowed=False,
            reason=(
                "Retrieved evidence is insufficient to answer "
                "the question reliably."
            ),
        )