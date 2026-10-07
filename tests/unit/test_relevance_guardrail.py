from medquery.guardrails.relevance import RelevanceGuardrail
from medquery.schemas.retrieval import RetrievalResult


def make_result(score: float) -> RetrievalResult:
    return RetrievalResult(
        chunk_id="test-chunk",
        document_id="test-document",
        text="Medical information about the query.",
        source="test",
        dense_score=score,
    )


def test_allows_strong_retrieval() -> None:
    guardrail = RelevanceGuardrail(
        min_top_score=0.30,
        min_top3_average=0.25,
    )

    results = [
        make_result(0.80),
        make_result(0.70),
        make_result(0.60),
    ]

    result = guardrail.check(results)

    assert result.allowed is True


def test_rejects_weak_retrieval() -> None:
    guardrail = RelevanceGuardrail(
        min_top_score=0.30,
        min_top3_average=0.25,
    )

    results = [
        make_result(0.20),
        make_result(0.18),
        make_result(0.15),
    ]

    result = guardrail.check(results)

    assert result.allowed is False


def test_rejects_empty_retrieval() -> None:
    guardrail = RelevanceGuardrail(
        min_top_score=0.30,
        min_top3_average=0.25,
    )

    result = guardrail.check([])

    assert result.allowed is False