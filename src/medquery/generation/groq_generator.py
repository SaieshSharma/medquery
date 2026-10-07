from groq import Groq


class GroqGenerator:
    def __init__(self, api_key: str, model_name: str) -> None:
        self.client = Groq(api_key=api_key)
        self.model_name = model_name

    def generate(self, prompt: str) -> str:
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            temperature=0.2,
            max_completion_tokens=256,
        )

        return response.choices[0].message.content or ""