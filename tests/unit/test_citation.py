from medquery.generation.citation import CitationValidator
from medquery.schemas.source import Source


def make_source(citation_id: int) -> Source:
    return Source(
        citation_id=citation_id,
        document_id=f"doc-{citation_id}",
        source="medquad",
        metadata={},
    )

def test_accepts_valid_citations() -> None:
    validator = CitationValidator()

    sources = [
        make_source(1),
        make_source(2),
        make_source(3),
    ]

    result = validator.validate(
        answer="Diabetes can cause thirst. [1] Frequent urination may occur. [2]",
        sources=sources,
    )

    assert result.valid is True
    assert result.citation_ids == [1, 2]
    assert result.invalid_citation_ids == []


def test_rejects_unknown_citation() -> None:
    validator = CitationValidator()

    sources = [
        make_source(1),
        make_source(2),
        make_source(3),
    ]

    result = validator.validate(
        answer="Diabetes can cause thirst. [1] Some claim. [7]",
        sources=sources,
    )

    assert result.valid is False
    assert result.citation_ids == [1, 7]
    assert result.invalid_citation_ids == [7]


def test_removes_duplicate_citations() -> None:
    validator = CitationValidator()

    sources = [
        make_source(1),
        make_source(2),
    ]

    result = validator.validate(
        answer="This is supported by [1][1][2][1].",
        sources=sources,
    )

    assert result.valid is True
    assert result.citation_ids == [1, 2]
    assert result.invalid_citation_ids == []


def test_handles_answer_without_citations() -> None:
    validator = CitationValidator()

    sources = [
        make_source(1),
        make_source(2),
    ]

    result = validator.validate(
        answer="There is not enough information to answer this.",
        sources=sources,
    )

    assert result.valid is True
    assert result.citation_ids == []
    assert result.invalid_citation_ids == []