from medquery.generation.groq_generator import GroqGenerator
from medquery.guardrails.relevance import RelevanceGuardrail
from medquery.retrieval.reranker import Reranker
from medquery.retrieval.retriever import Retriever
from medquery.schemas.response import RAGResponse


class RAGPipeline:
    def __init__(
        self,
        retriever: Retriever,
        reranker: Reranker,
        generator: GroqGenerator,
        relevance_guardrail: RelevanceGuardrail,
    ) -> None:
        self.retriever = retriever
        self.reranker = reranker
        self.generator = generator
        self.relevance_guardrail = relevance_guardrail

    def run(
        self,
        query: str,
        retrieval_k: int = 10,
        final_k: int = 5,
    ) -> RAGResponse:
        retrieved_results = self.retriever.retrieve(
            query=query,
            top_k=retrieval_k,
        )

        guardrail_result = self.relevance_guardrail.check(
            retrieved_results
        )

        if not guardrail_result.allowed:
            return RAGResponse(
                answer=(
                    "I don't have enough relevant medical information "
                    "in my knowledge base to answer this question reliably."
                ),
                sources=[],
            )

        reranked_results = self.reranker.rerank(
            query=query,
            results=retrieved_results,
            top_k=final_k,
        )

        answer = self.generator.generate(
            query=query,
            results=reranked_results,
        )

        return RAGResponse(
            answer=answer,
            sources=reranked_results,
        )