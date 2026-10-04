import numpy as np

from medquery.config.settings import settings
from medquery.embeddings.model import EmbeddingModel


def cosine_similarity(
    vector_a: list[float],
    vector_b: list[float],
) -> float:
    a = np.array(vector_a)
    b = np.array(vector_b)

    return float(np.dot(a, b))


def main() -> None:
    embedding_model = EmbeddingModel(settings.embedding_model)

    texts = [
        "What are the symptoms of diabetes?",
        "What signs can indicate diabetes?",
        "How do I bake a chocolate cake?",
    ]

    embeddings = embedding_model.embed_batch(texts)

    similarity_01 = cosine_similarity(embeddings[0], embeddings[1])
    similarity_02 = cosine_similarity(embeddings[0], embeddings[2])

    print(f"Similarity between medical questions: {similarity_01:.4f}")
    print(f"Similarity between medical and unrelated question: {similarity_02:.4f}")


if __name__ == "__main__":
    main()