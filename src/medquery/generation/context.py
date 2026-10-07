from dataclasses import dataclass

from medquery.schemas.retrieval import RetrievalResult
from medquery.schemas.source import Source


@dataclass
class Context:
    text: str
    sources: list[Source]


class ContextBuilder:
    def build(
        self,
        results: list[RetrievalResult],
    ) -> Context:
        context_parts: list[str] = []
        sources: list[Source] = []

        for citation_id, result in enumerate(results, start=1):
            context_parts.append(
                f"[{citation_id}]\n{result.text}"
            )

            metadata = result.metadata


            sources.append(
                Source(
                    citation_id=citation_id,
                    document_id=result.document_id,
                    source=result.source,
                    source_name=metadata.get("source_name"),
                    focus=metadata.get("focus"),
                    url=metadata.get("url"),
                )
            )

        return Context(
            text="\n\n".join(context_parts),
            sources=sources,
        )