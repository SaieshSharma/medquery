from medquery.config.settings import settings
from medquery.embeddings.model import EmbeddingModel
from medquery.retrieval.qdrant_store import QdrantVectorStore
from medquery.retrieval.reranker import Reranker
from medquery.retrieval.retriever import Retriever

TEST_QUERIES = [
    # Clearly medical
    ("What are the symptoms of diabetes?", "medical"),
    ("What is insulin?", "medical"),
    ("What causes headaches?", "medical"),
    ("What are the symptoms of pneumonia?", "medical"),
    ("What is high blood pressure?", "medical"),
    ("How does insulin work?", "medical"),
    ("What causes anemia?", "medical"),

    # Indirect medical
    ("Why do I feel tired all the time?", "medical"),
    ("Why am I dizzy when I stand up?", "medical"),
    ("Why am I coughing at night?", "medical"),
    ("How can I improve my sleep?", "medical"),
    ("What foods are good for my health?", "medical"),

    # Clearly non-medical
    ("Who won the cricket match?", "non-medical"),
    ("What is the capital of France?", "non-medical"),
    ("How do I sort an array in Java?", "non-medical"),
    ("How does TCP work?", "non-medical"),
    ("How do I make pasta?", "non-medical"),
    ("How does a car engine work?", "non-medical"),

    # Ambiguous but intended medical
    ("Why does my heart race sometimes?", "medical"),
    ("Why can't I concentrate?", "medical"),
    ("Why am I gaining weight?", "medical"),
    ("Why do I feel weak?", "medical"),
]


def main() -> None:
    embedding_model = EmbeddingModel(
        settings.embedding_model
    )

    vector_size = len(
        embedding_model.embed("test")
    )

    vector_store = QdrantVectorStore(
        url=settings.qdrant_url,
        collection_name=settings.qdrant_collection,
        vector_size=vector_size,
    )

    retriever = Retriever(
        embedding_model=embedding_model,
        vector_store=vector_store,
    )

    reranker = Reranker(
        settings.reranker_model
    )

    for query, expected in TEST_QUERIES:
        print("\n" + "=" * 70)
        print(f"Query:    {query}")
        print(f"Expected: {expected}")

        retrieved_results = retriever.retrieve(
            query=query,
            top_k=10,
        )

        top_dense = retrieved_results[0].dense_score

        top_3_avg = sum(
            result.dense_score
            for result in retrieved_results[:3]
        ) / 3

        top_10_avg = sum(
            result.dense_score
            for result in retrieved_results
        ) / len(retrieved_results)

        reranked_results = reranker.rerank(
            query=query,
            results=retrieved_results,
            top_k=3,
        )

        top_rerank = reranked_results[0].rerank_score

        print(
            f"top_dense={top_dense:.4f} | "
            f"top3_avg={top_3_avg:.4f} | "
            f"top10_avg={top_10_avg:.4f} | "
            f"top_rerank={top_rerank:.4f}"
        )

        print("\nDense retrieval:")
        for rank, result in enumerate(
            retrieved_results,
            start=1,
        ):
            print(
                f"  #{rank} "
                f"dense={result.dense_score:.4f} "
                f"document={result.document_id}"
            )

        print("\nAfter reranking:")
        for rank, result in enumerate(
            reranked_results,
            start=1,
        ):
            print(
                f"  #{rank} "
                f"dense={result.dense_score:.4f} "
                f"rerank={result.rerank_score:.4f} "
                f"document={result.document_id}"
            )


if __name__ == "__main__":
    main()