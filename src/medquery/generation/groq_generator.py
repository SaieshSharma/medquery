from groq import Groq

from medquery.generation.context import Context


class GroqGenerator:
    def __init__(self, api_key: str, model_name: str) -> None:
        self.client = Groq(api_key=api_key)
        self.model_name = model_name

    def generate(
        self,
        query: str,
        context: Context,
    ) -> str:
        system_prompt = """
You are MedQuery, a medical question-answering assistant.

Answer the user's question using only the provided context.

Rules:
1. Do not invent facts that are not supported by the context.
2. If the context is insufficient to answer the question, clearly say so.
3. Give a concise and understandable answer.
4. Do not present unsupported medical advice as fact.
5. When making a factual claim, place the citation immediately after
   the sentence or claim it supports, such as:
   "Frequent urination is a common symptom. [1]"
6. Do not put all citations together at the end of the answer.
7. Only use citation numbers that actually exist in the provided context.
8. If multiple sources support the same claim, you may cite them together,
   such as [1][2].
""".strip()

        user_prompt = f"""
    User question:
    {query}

    Retrieved context:
    {context.text}
    """.strip()

        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.2,
            max_completion_tokens=512,
        )

        return response.choices[0].message.content or ""
