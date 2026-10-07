from medquery.generation.context import ContextBuilder
from medquery.schemas.retrieval import RetrievalResult


def make_result(
    document_id: str,
    text: str,
) -> RetrievalResult:
    return RetrievalResult(
        chunk_id=f"{document_id}-0",
        document_id=document_id,
        text=text,
        source="medquad",
        dense_score=0.8,
    )


def test_builds_numbered_context() -> None:
    results = [
        make_result("doc-1", "Information about diabetes."),
        make_result("doc-2", "Information about insulin."),
    ]

    context = ContextBuilder().build(results)

    assert "[1]\nInformation about diabetes." in context.text
    assert "[2]\nInformation about insulin." in context.text


def test_creates_matching_sources() -> None:
    results = [
        make_result("doc-1", "Information about diabetes."),
        make_result("doc-2", "Information about insulin."),
    ]

    context = ContextBuilder().build(results)

    assert len(context.sources) == 2

    assert context.sources[0].citation_id == 1
    assert context.sources[0].document_id == "doc-1"

    assert context.sources[1].citation_id == 2
    assert context.sources[1].document_id == "doc-2"


def test_empty_results_produce_empty_context() -> None:
    context = ContextBuilder().build([])

    assert context.text == ""
    assert context.sources == []

def test_maps_metadata_to_source_fields() -> None:
    result = RetrievalResult(
        chunk_id="doc-1-0",
        document_id="doc-1",
        text="Information about diabetes.",
        source="medquad",
        dense_score=0.8,
        metadata={
            "source_name": "NIHSeniorHealth",
            "focus": "Diabetes",
            "url": "https://example.com/diabetes",
        },
    )

    context = ContextBuilder().build([result])

    source = context.sources[0]

    assert source.source_name == "NIHSeniorHealth"
    assert source.focus == "Diabetes"
    assert source.url == "https://example.com/diabetes"