from pathlib import Path

from medquery.config.settings import settings
from medquery.embeddings.model import EmbeddingModel
from medquery.ingestion.medquad import load_medquad
from medquery.retrieval.qdrant_store import QdrantVectorStore


def main() -> None:
    documents = load_medquad(
        data_dir=Path(settings.medquad_data_dir),
        require_answers=True,
    )

    test_documents = documents[:3]

    embedding_model = EmbeddingModel(settings.embedding_model)

    texts = [document.text for document in test_documents]
    vectors = embedding_model.embed_batch(texts)

    vector_store = QdrantVectorStore(
        url=settings.qdrant_url,
        collection_name=settings.qdrant_collection,
        vector_size=len(vectors[0]),
    )

    vector_store.ensure_collection()

    points = []

    for document, vector in zip(test_documents, vectors):
        payload = {
            "text": document.text,
            "source": document.source,
            "document_id": document.document_id,
            **document.metadata,
        }

        points.append(
            (
                document.document_id,
                vector,
                payload,
            )
        )

    vector_store.upsert_batch(points)

    print(f"Successfully upserted {len(points)} documents.")
    print(f"Vector dimensions: {len(vectors[0])}")


if __name__ == "__main__":
    main()