from dataclasses import dataclass


@dataclass
class Source:
    citation_id: int
    document_id: str
    source: str
    source_name: str | None
    focus: str | None
    url: str | None