from dataclasses import dataclass

from medquery.schemas.source import Source


@dataclass
class RAGResponse:
    answer: str
    sources: list[Source]
    status: str