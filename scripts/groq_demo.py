
from medquery.config.settings import settings
from medquery.generation.groq_generator import GroqGenerator


def main() -> None:
    if not settings.groq_api_key:
        raise RuntimeError("GROQ_API_KEY is not configured.")

    generator = GroqGenerator(
        api_key=settings.groq_api_key,
        model_name=settings.groq_model,
    )

    answer = generator.generate(
        "In one sentence, explain what diabetes is."
    )

    print("\nGroq response:\n")
    print(answer)


if __name__ == "__main__":
    main()