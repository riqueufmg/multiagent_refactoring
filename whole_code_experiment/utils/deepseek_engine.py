import os
from dotenv import load_dotenv
from openai import OpenAI
import tiktoken

class DeepSeekEngine:
    def __init__(
        self,
        model_name: str,
        max_input_tokens: int = 2048,
        max_completion_tokens: int = 4096
    ):
        self.model_name = model_name
        self.max_input_tokens = max_input_tokens
        self.max_completion_tokens = max_completion_tokens

        load_dotenv()
        self.api_key = os.getenv("DEEPSEEK_API_KEY")

        if not self.api_key:
            raise EnvironmentError("DEEPSEEK_API_KEY not found in environment variables")

        self.client = OpenAI(
            api_key=self.api_key,
            base_url="https://api.deepseek.com"
        )

    def generate(self, prompt_text: str) -> str:
        encoding = tiktoken.get_encoding("o200k_base")
        prompt_len = len(encoding.encode(prompt_text))

        if prompt_len > self.max_input_tokens:
            raise ValueError(
                f"Prompt exceeds the maximum input tokens ({self.max_input_tokens})"
            )

        response = self.client.chat.completions.create(
            model=self.model_name,  # ex: "deepseek-chat" ou "deepseek-reasoner"
            temperature=0.1,
            messages=[
                {"role": "user", "content": prompt_text}
            ],
            max_tokens=self.max_completion_tokens
        )

        return response.choices[0].message.content.strip()
