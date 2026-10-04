from medquery.config.settings import settings
from medquery.embeddings.model import EmbeddingModel
from medquery.retrieval.qdrant_store import QdrantVectorStore
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

    results = retriever.retrieve(
        query=query,
        top_k=5,
    )

    print(f"\nQuery: {query}")
    print(f"Retrieved {len(results)} results.")

    for index, result in enumerate(results, start=1):
        print(f"\n--- Result {index} ---")
        print(f"Score: {result.score:.4f}")
        print(f"Document ID: {result.document_id}")
        print(f"Chunk ID: {result.chunk_id}")
        print(f"Source: {result.source}")
        print(f"Text:\n{result.text[:1000]}")


if __name__ == "__main__":
    main()