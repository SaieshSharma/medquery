from dataclasses import dataclass, field
from typing import Any


@dataclass
class RetrievalResult:
    chunk_id: str
    document_id: str
    text: str
    score: float
    source: str
    metadata: dict[str, Any] = field(default_factory=dict)