from dataclasses import dataclass

from medquery.schemas.retrieval import RetrievalResult


@dataclass
class RAGResponse:
    answer: str
    sources: list[RetrievalResult]