import os
from dotenv import load_dotenv
import openai
import tiktoken

class GPTEngine:
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
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.client = openai.OpenAI(api_key=self.api_key)

    def generate(self, prompt_text):
        encoding = tiktoken.get_encoding("o200k_base")
        prompt_len = len(encoding.encode(prompt_text))

        if prompt_len > self.max_input_tokens:
            raise ValueError(f"Prompt exceeds the maximum input tokens ({self.max_input_tokens})")

        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[{"role": "user", "content": prompt_text}],
            max_completion_tokens=self.max_completion_tokens
        )

        return response.choices[0].message.content.strip()