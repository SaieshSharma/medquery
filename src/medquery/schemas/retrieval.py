from dataclasses import dataclass, field
from typing import Any


@dataclass
class RetrievalResult:
    chunk_id: str
    document_id: str
    text: str
    source: str

    dense_score: float
    rerank_score: float | None = None

    metadata: dict[str, Any] = field(default_factory=dict)