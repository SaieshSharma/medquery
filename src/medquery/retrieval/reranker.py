from sentence_transformers import CrossEncoder

from medquery.schemas.retrieval import RetrievalResult


class Reranker:
    def __init__(self, model_name: str) -> None:
        self.model = CrossEncoder(model_name)

    def rerank(
        self,
        query: str,
        results: list[RetrievalResult],
        top_k: int = 5,
    ) -> list[RetrievalResult]:
        pairs = [[query, result.text] for result in results]

        scores = self.model.predict(pairs)

        ranked_results = sorted(
            zip(results, scores),
            key=lambda item: float(item[1]),
            reverse=True,
        )

        reranked_results = []

        for result, score in ranked_results[:top_k]:
            result.rerank_score = float(score)
            reranked_results.append(result)

        return reranked_results