from pathlib import Path

from medquery.ingestion.chunker import chunk_documents
from medquery.ingestion.medquad import load_medquad


def main() -> None:
    data_dir = Path("data/raw/MedQuAD")

    documents = load_medquad(data_dir)
    chunks = chunk_documents(documents)

    print(f"Documents: {len(documents)}")
    print(f"Chunks: {len(chunks)}")

    for chunk in chunks[:3]:
        print("\n---")
        print(f"Chunk ID: {chunk.chunk_id}")
        print(f"Document ID: {chunk.document_id}")
        print(f"Source: {chunk.source}")
        print(f"Text:\n{chunk.text}")


if __name__ == "__main__":
    main()