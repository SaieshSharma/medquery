from medquery.config.settings import settings
from medquery.embeddings.model import EmbeddingModel
from medquery.generation.groq_generator import GroqGenerator
from medquery.pipeline.rag_pipeline import RAGPipeline
from medquery.retrieval.qdrant_store import QdrantVectorStore
from medquery.retrieval.reranker import Reranker
from medquery.retrieval.retriever import Retriever


def main() -> None:
    if not settings.groq_api_key:
        raise RuntimeError("GROQ_API_KEY is not configured.")

    embedding_model = EmbeddingModel(settings.embedding_model)

    vector_size = len(embedding_model.embed("test"))

    vector_store = QdrantVectorStore(
        url=settings.qdrant_url,
        collection_name=settings.qdrant_collection,
        vector_size=vector_size,
    )

    retriever = Retriever(
        embedding_model=embedding_model,
        vector_store=vector_store,
    )

    reranker = Reranker(settings.reranker_model)

    generator = GroqGenerator(
        api_key=settings.groq_api_key,
        model_name=settings.groq_model,
    )

    pipeline = RAGPipeline(
        retriever=retriever,
        reranker=reranker,
        generator=generator,
    )

    query = "What are the symptoms of diabetes?"

    print(f"\nQuestion: {query}\n")

    response = pipeline.run(
        query=query,
        retrieval_k=10,
        final_k=5,
    )

    print("Answer:")
    print(response.answer)

    print("\nSources:")

    for index, result in enumerate(response.sources, start=1):
        print(f"\n[{index}]")
        print(f"Source: {result.source}")
        print(f"Document: {result.document_id}")

        source_name = result.metadata.get("source_name")
        url = result.metadata.get("url")
        focus = result.metadata.get("focus")

        if source_name:
            print(f"Source name: {source_name}")

        if focus:
            print(f"Focus: {focus}")

        if url:
            print(f"URL: {url}")


if __name__ == "__main__":
    main()