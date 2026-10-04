from medquery.schemas.chunk import Chunk
from medquery.schemas.document import Document


def chunk_documents(documents: list[Document]) -> list[Chunk]:
    chunks: list[Chunk] = []

    for document in documents:
        chunks.append(
            Chunk(
                text=document.text,
                chunk_id=f"{document.document_id}-0",
                document_id=document.document_id,
                source=document.source,
                metadata=document.metadata.copy(),
            )
        )

    return chunks