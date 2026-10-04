from medquery.config.settings import settings
from medquery.embeddings.model import EmbeddingModel


def main() -> None:
    embedding_model = EmbeddingModel(settings.embedding_model)

    texts = [
        "What are the symptoms of diabetes?",
        "What signs can indicate diabetes?",
        "How do I make chocolate cake?",
    ]

    embeddings = embedding_model.embed_batch(texts)

    for text, embedding in zip(texts, embeddings):
        print(f"\nText: {text}")
        print(f"Dimensions: {len(embedding)}")
        print(f"First 5 values: {embedding[:5]}")


if __name__ == "__main__":
    main()