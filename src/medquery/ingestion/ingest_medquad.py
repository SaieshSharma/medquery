from pathlib import Path

from medquery.config.settings import settings
from medquery.embeddings.model import EmbeddingModel
from medquery.ingestion.chunker import chunk_documents
from medquery.ingestion.medquad import load_medquad
from medquery.retrieval.qdrant_store import QdrantVectorStore

BATCH_SIZE = 64


def main() -> None:
    print("Loading MedQuAD dataset...")

    documents = load_medquad(
        data_dir=Path(settings.medquad_data_dir),
        require_answers=True,
    )

    print(f"Loaded {len(documents)} documents.")

    print("Creating chunks...")

    chunks = chunk_documents(documents)

    print(f"Created {len(chunks)} chunks.")

    print("Loading embedding model...")

    embedding_model = EmbeddingModel(settings.embedding_model)

    vector_size = len(embedding_model.embed("test"))

    print(f"Embedding dimensions: {vector_size}")

    vector_store = QdrantVectorStore(
        url=settings.qdrant_url,
        collection_name=settings.qdrant_collection,
        vector_size=vector_size,
    )

    vector_store.ensure_collection()

    total_chunks = len(chunks)

    for start in range(0, total_chunks, BATCH_SIZE):
        batch = chunks[start : start + BATCH_SIZE]

        texts = [chunk.text for chunk in batch]

        vectors = embedding_model.embed_batch(texts)

        points = []

        for chunk, vector in zip(batch, vectors):
            payload = {
                "text": chunk.text,
                "chunk_id": chunk.chunk_id,
                "document_id": chunk.document_id,
                "source": chunk.source,
                **chunk.metadata,
            }

            points.append(
                (
                    chunk.chunk_id,
                    vector,
                    payload,
                )
            )

        vector_store.upsert_batch(points)

        processed = min(start + BATCH_SIZE, total_chunks)

        print(
            f"Processed {processed}/{total_chunks} "
            f"({processed / total_chunks:.1%})"
        )

    print("\nMedQuAD ingestion completed successfully.")


if __name__ == "__main__":
    main()