from transformers import AutoTokenizer, AutoModelForCausalLM
from dotenv import load_dotenv
from pathlib import Path
import os
import torch

class LLMInferenceEngine:

    def __init__(
        self,
        model_name_or_path: str,
        max_input_tokens: int = 1024,
        max_total_tokens: int = 2048,
        temperature: float = 0.1,
        top_k: int = 50,
        top_p: float = 0.95
    ):
        self.model_name_or_path = model_name_or_path
        self.max_input_tokens = max_input_tokens
        self.max_total_tokens = max_total_tokens
        self.temperature = temperature
        self.top_k = top_k
        self.top_p = top_p

        load_dotenv()
        self.hf_token = os.getenv("HF_TOKEN")

        self.tokenizer = None
        self.model = None

    def load_model(self):
        llm_path = Path("tools", "llms", self.model_name_or_path.replace("/", "_"))

        if not llm_path.exists() or not any(llm_path.iterdir()):
            llm_path.mkdir(parents=True, exist_ok=True)

            tokenizer = AutoTokenizer.from_pretrained(self.model_name_or_path, token=self.hf_token)
            tokenizer.save_pretrained(llm_path)

            model = AutoModelForCausalLM.from_pretrained(
                self.model_name_or_path, 
                token=self.hf_token
            )
            model.save_pretrained(llm_path)

            print(f"Model and tokenizer saved at {llm_path}")

        self.tokenizer = AutoTokenizer.from_pretrained(llm_path)

        self.model = AutoModelForCausalLM.from_pretrained(
            llm_path,
            device_map="auto",
            load_in_8bit=True
        )

    def prompt_fits(self, prompt_text):
        prompt_len = len(self.tokenizer.encode(prompt_text))
        print(f"Prompt length: {prompt_len}")
        return prompt_len <= self.max_input_tokens
    
    def generate(self, prompt_text):
        if not self.prompt_fits(prompt_text):
            raise ValueError(f"Prompt exceeds the maximum input tokens ({self.max_input_tokens})")
        
        inputs = self.tokenizer(prompt_text, return_tensors="pt").to(self.model.device)
        
        outputs = self.model.generate(
            **inputs,
            max_new_tokens=self.max_total_tokens - inputs.input_ids.shape[1],
            temperature=self.temperature,
            top_k=self.top_k,
            top_p=self.top_p,
            no_repeat_ngram_size=3,
            repetition_penalty=1.2
        )
        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)