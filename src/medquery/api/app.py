from fastapi import FastAPI

from medquery.api.dependencies import create_rag_pipeline
from medquery.api.mapper import to_query_response
from medquery.api.schemas import QueryRequest, QueryResponse

app = FastAPI(
    title="MedQuery API",
    description=(
        "Retrieval-Augmented Generation API for grounded "
        "medical question answering."
    ),
    version="0.1.0",
)

pipeline = create_rag_pipeline()


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/query", response_model=QueryResponse)
def query(request: QueryRequest) -> QueryResponse:
    response = pipeline.run(query=request.question)
    return to_query_response(response)