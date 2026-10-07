from medquery.guardrails.relevance import RelevanceGuardrail
from medquery.pipeline.rag_pipeline import RAGPipeline
from medquery.schemas.retrieval import RetrievalResult


class FakeRetriever:
    def retrieve(
        self,
        query: str,
        top_k: int = 5,
    ) -> list[RetrievalResult]:
        return [
            RetrievalResult(
                chunk_id="chunk-1",
                document_id="doc-1",
                text="Diabetes can cause increased thirst.",
                source="medquad",
                dense_score=0.80,
            ),
            RetrievalResult(
                chunk_id="chunk-2",
                document_id="doc-2",
                text="Diabetes can cause frequent urination.",
                source="medquad",
                dense_score=0.70,
            ),
            RetrievalResult(
                chunk_id="chunk-3",
                document_id="doc-3",
                text="Diabetes can cause fatigue.",
                source="medquad",
                dense_score=0.60,
            ),
        ]


class FakeReranker:
    def rerank(
        self,
        query: str,
        results: list[RetrievalResult],
        top_k: int = 5,
    ) -> list[RetrievalResult]:
        return results[:top_k]


class FakeGenerator:
    def __init__(self) -> None:
        self.received_context = None

    def generate(self, query: str, context) -> str:
        self.received_context = context
        return "Diabetes can cause increased thirst. [1]"


def test_pipeline_returns_sources_from_generation_context() -> None:
    generator = FakeGenerator()

    pipeline = RAGPipeline(
        retriever=FakeRetriever(),
        reranker=FakeReranker(),
        generator=generator,
        relevance_guardrail=RelevanceGuardrail(
            min_top_score=0.30,
            min_top3_average=0.25,
        ),
    )

    response = pipeline.run(
        query="What are symptoms of diabetes?",
        retrieval_k=3,
        final_k=3,
    )

    assert response.answer == "Diabetes can cause increased thirst. [1]"
    assert response.status == "answered"
    assert len(response.sources) == 3

    assert response.sources[0].citation_id == 1
    assert response.sources[0].document_id == "doc-1"

    assert response.sources[1].citation_id == 2
    assert response.sources[1].document_id == "doc-2"

    assert response.sources[2].citation_id == 3
    assert response.sources[2].document_id == "doc-3"

    assert generator.received_context is not None
    assert generator.received_context.sources == response.sources



class InvalidCitationGenerator:
    def generate(self, query: str, context) -> str:
        return "Diabetes can cause increased thirst. [999]"



def test_pipeline_rejects_invalid_citations() -> None:
    pipeline = RAGPipeline(
        retriever=FakeRetriever(),
        reranker=FakeReranker(),
        generator=InvalidCitationGenerator(),
        relevance_guardrail=RelevanceGuardrail(
            min_top_score=0.30,
            min_top3_average=0.25,
        ),
    )

    response = pipeline.run(
        query="What are symptoms of diabetes?",
        retrieval_k=3,
        final_k=3,
    )

    assert response.answer == (
        "I couldn't generate a reliably cited answer "
        "from the available medical sources."
    )
    assert response.status == "abstained"
    assert response.sources == []


class EmptyEvidenceRetriever:
    def retrieve(
        self,
        query: str,
        top_k: int = 5,
    ) -> list[RetrievalResult]:
        return [
            RetrievalResult(
                chunk_id="chunk-1",
                document_id="doc-1",
                text="Some unrelated information.",
                source="medquad",
                dense_score=0.10,
            ),
            RetrievalResult(
                chunk_id="chunk-2",
                document_id="doc-2",
                text="More unrelated information.",
                source="medquad",
                dense_score=0.12,
            ),
            RetrievalResult(
                chunk_id="chunk-3",
                document_id="doc-3",
                text="More unrelated information.",
                source="medquad",
                dense_score=0.15,
            ),
        ]


def test_pipeline_abstains_when_evidence_is_insufficient() -> None:
    pipeline = RAGPipeline(
        retriever=EmptyEvidenceRetriever(),
        reranker=FakeReranker(),
        generator=FakeGenerator(),
        relevance_guardrail=RelevanceGuardrail(
            min_top_score=0.30,
            min_top3_average=0.25,
        ),
    )

    response = pipeline.run(
        query="What is the capital of France?",
        retrieval_k=3,
        final_k=3,
    )

    assert response.status == "abstained"
    assert response.sources == []
    assert response.answer == (
        "I don't have enough relevant medical information "
        "in my knowledge base to answer this question reliably."
    )