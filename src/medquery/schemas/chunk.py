from dataclasses import dataclass, field
from typing import Any


@dataclass
class Chunk:
    text: str
    chunk_id: str
    document_id: str
    source: str
    metadata: dict[str, Any] = field(default_factory=dict)