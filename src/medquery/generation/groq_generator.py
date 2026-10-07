from groq import Groq

from medquery.schemas.retrieval import RetrievalResult


class GroqGenerator:
    def __init__(self, api_key: str, model_name: str) -> None:
        self.client = Groq(api_key=api_key)
        self.model_name = model_name

    def generate(
        self,
        query: str,
        results: list[RetrievalResult],
    ) -> str:
        context_parts = []

        for index, result in enumerate(results, start=1):
            context_parts.append(
                f"[Source {index}]\n{result.text}"
            )

        context = "\n\n".join(context_parts)

        system_prompt = """
You are MedQuery, a medical question-answering assistant.

Answer the user's question using only the provided context.

Rules:
1. Do not invent facts that are not supported by the context.
2. If the context is insufficient to answer the question, clearly say so.
3. Give a concise and understandable answer.
4. Do not present unsupported medical advice as fact.
""".strip()

        user_prompt = f"""
User question:
{query}

Retrieved context:
{context}
""".strip()

        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[
                {
                    "role": "system",
                    "content": system_prompt,
                },
                {
                    "role": "user",
                    "content": user_prompt,
                },
            ],
            temperature=0.2,
            max_completion_tokens=512,
        )

        return response.choices[0].message.content or ""