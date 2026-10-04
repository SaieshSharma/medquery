from medquery.config.settings import settings
from medquery.embeddings.model import EmbeddingModel
from medquery.retrieval.qdrant_store import QdrantVectorStore
from medquery.retrieval.reranker import Reranker
from medquery.retrieval.retriever import Retriever


def main() -> None:
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

    query = "What are the symptoms of diabetes?"

    candidates = retriever.retrieve(
        query=query,
        top_k=10,
    )

    reranker = Reranker(settings.reranker_model)

    results = reranker.rerank(
        query=query,
        results=candidates,
        top_k=5,
    )

    print(f"\nQuery: {query}")
    print(f"Candidates retrieved: {len(candidates)}")
    print(f"Results after reranking: {len(results)}")

    for index, result in enumerate(results, start=1):
        print(f"\n--- Result {index} ---")
        print(f"Document ID: {result.document_id}")
        print(f"Chunk ID: {result.chunk_id}")
        print(f"Source: {result.source}")
        print(f"Text:\n{result.text[:1000]}")


if __name__ == "__main__":
    main()