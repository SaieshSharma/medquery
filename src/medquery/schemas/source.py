from dataclasses import dataclass
from typing import Any


@dataclass
class Source:
    citation_id: int
    document_id: str
    source: str
    metadata: dict[str, Any]