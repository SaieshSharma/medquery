from medquery.embeddings.model import EmbeddingModel
from medquery.retrieval.qdrant_store import QdrantVectorStore
from medquery.schemas.retrieval import RetrievalResult


class Retriever:
    def __init__(
        self,
        embedding_model: EmbeddingModel,
        vector_store: QdrantVectorStore,
    ) -> None:
        self.embedding_model = embedding_model
        self.vector_store = vector_store

    def retrieve(
        self,
        query: str,
        top_k: int = 5,
    ) -> list[RetrievalResult]:
        query_vector = self.embedding_model.embed(query)

        qdrant_results = self.vector_store.search(
            query_vector=query_vector,
            limit=top_k,
        )

        results = []

        for result in qdrant_results:
            payload = result.payload

            results.append(
                RetrievalResult(
                    chunk_id=payload["chunk_id"],
                    document_id=payload["document_id"],
                    text=payload["text"],
                    dense_score=float(result.score),
                    source=payload["source"],
                    metadata={
                        key: value
                        for key, value in payload.items()
                        if key not in {
                            "chunk_id",
                            "document_id",
                            "text",
                            "source",
                        }
                    },
                )
            )

        return results