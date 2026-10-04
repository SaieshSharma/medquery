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

    document = documents[0]

    embedding_model = EmbeddingModel(settings.embedding_model)

    vector = embedding_model.embed(document.text)

    vector_store = QdrantVectorStore(
        url=settings.qdrant_url,
        collection_name=settings.qdrant_collection,
        vector_size=len(vector),
    )

    vector_store.ensure_collection()

    vector_store.upsert(
        point_id=document.document_id,
        vector=vector,
        payload={
            "text": document.text,
            "source": document.source,
            "document_id": document.document_id,
            **document.metadata,
        },
    )

    print("Successfully stored first MedQuAD document in Qdrant.")
    print(f"Document ID: {document.document_id}")
    print(f"Vector dimensions: {len(vector)}")


if __name__ == "__main__":
    main()