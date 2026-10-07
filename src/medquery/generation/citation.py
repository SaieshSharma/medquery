import re

from medquery.schemas.citation import CitationValidationResult
from medquery.schemas.source import Source


class CitationValidator:
    CITATION_PATTERN = re.compile(r"\[(\d+)\]")

    def validate(
        self,
        answer: str,
        sources: list[Source],
    ) -> CitationValidationResult:
        matches = self.CITATION_PATTERN.findall(answer)

        citation_ids = sorted(
            {int(match) for match in matches}
        )

        valid_source_ids = {
            source.citation_id
            for source in sources
        }

        invalid_citation_ids = [
            citation_id
            for citation_id in citation_ids
            if citation_id not in valid_source_ids
        ]

        return CitationValidationResult(
            valid=not invalid_citation_ids,
            citation_ids=citation_ids,
            invalid_citation_ids=invalid_citation_ids,
        )