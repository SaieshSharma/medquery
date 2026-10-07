from typing import Literal

from pydantic import BaseModel, Field


class QueryRequest(BaseModel):
    question: str = Field(min_length=1)


class SourceResponse(BaseModel):
    citation_id: int
    document_id: str
    source: str
    source_name: str | None
    focus: str | None
    url: str | None


class QueryResponse(BaseModel):
    answer: str
    status: Literal["answered", "abstained"]
    sources: list[SourceResponse]