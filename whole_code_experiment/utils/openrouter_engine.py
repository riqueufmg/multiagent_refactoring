import os
import requests
from dotenv import load_dotenv
import tiktoken

class OpenRouterEngine:

    def __init__(
        self,
        model: str,
        max_input_tokens: int = 200_000,
        max_output_tokens: int = 4096,
        temperature: float = 0.2
    ):
        self.model = model
        self.max_input_tokens = max_input_tokens
        self.max_output_tokens = max_output_tokens
        self.temperature = temperature

        load_dotenv()
        self.api_key = os.getenv("OPENROUTER_API_KEY")

        if not self.api_key:
            raise EnvironmentError("OPENROUTER_API_KEY not found in environment (.env)")

        self.endpoint = "https://openrouter.ai/api/v1/chat/completions"

    def count_tokens(self, text: str) -> int:
        encoding = tiktoken.get_encoding("o200k_base")  # universal encoder
        return len(encoding.encode(text))

    def generate(self, prompt_text: str, system_prompt: str | None = None) -> str:
        prompt_len = self.count_tokens(prompt_text)

        if prompt_len > self.max_input_tokens:
            raise ValueError(f"Prompt exceeds max input tokens ({self.max_input_tokens}). Size: {prompt_len}")

        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})

        messages.append({"role": "user", "content": prompt_text})

        response = requests.post(
            self.endpoint,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": self.model,
                "messages": messages,
                "max_tokens": self.max_output_tokens,
                "temperature": self.temperature
            }
        )

        if response.status_code != 200:
            raise RuntimeError(
                f"OpenRouter API error ({response.status_code}): {response.text}"
            )

        data = response.json()

        try:
            return data["choices"][0]["message"]["content"].strip()
        except Exception:
            raise RuntimeError("Unexpected OpenRouter response format:\n" + str(data))
