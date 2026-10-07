from medquery.api.schemas import QueryResponse, SourceResponse
from medquery.schemas.response import RAGResponse


def to_query_response(response: RAGResponse) -> QueryResponse:
    sources = [
        SourceResponse(
            citation_id=source.citation_id,
            document_id=source.document_id,
            source=source.source,
            source_name=source.source_name,
            focus=source.focus,
            url=source.url,
        )
        for source in response.sources
    ]

    return QueryResponse(
        answer=response.answer,
        status=response.status,
        sources=sources,
    )