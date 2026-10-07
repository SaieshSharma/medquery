from medquery.config.settings import settings
from medquery.embeddings.model import EmbeddingModel
from medquery.generation.groq_generator import GroqGenerator
from medquery.guardrails.relevance import RelevanceGuardrail
from medquery.pipeline.rag_pipeline import RAGPipeline
from medquery.retrieval.qdrant_store import QdrantVectorStore
from medquery.retrieval.reranker import Reranker
from medquery.retrieval.retriever import Retriever


def create_rag_pipeline() -> RAGPipeline:
    embedding_model = EmbeddingModel(settings.embedding_model)

    vector_store = QdrantVectorStore(
        url=settings.qdrant_url,
        collection_name=settings.qdrant_collection,
        vector_size=384,
    )

    retriever = Retriever(
        embedding_model=embedding_model,
        vector_store=vector_store,
    )

    reranker = Reranker(settings.reranker_model)

    generator = GroqGenerator(
        api_key=settings.groq_api_key or "",
        model_name=settings.groq_model,
    )

    relevance_guardrail = RelevanceGuardrail(
        min_top_score=0.30,
        min_top3_average=0.25,
    )

    return RAGPipeline(
        retriever=retriever,
        reranker=reranker,
        generator=generator,
        relevance_guardrail=relevance_guardrail,
    )