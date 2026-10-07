from dataclasses import dataclass


@dataclass
class CitationValidationResult:
    valid: bool
    citation_ids: list[int]
    invalid_citation_ids: list[int]