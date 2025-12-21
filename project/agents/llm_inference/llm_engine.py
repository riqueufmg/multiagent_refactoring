from transformers import AutoTokenizer, AutoModelForCausalLM

class LLMInferenceEngine:

    def __init__(
        self,
        model_name_or_path: str,
        max_input_tokens: int = 2048,
        max_total_tokens: int = 4096,
        temperature: float = 0.7,
        top_k: int = 50,
        top_p: float = 0.9
    ):
        self.model_name_or_path = model_name_or_path
        self.max_input_tokens = max_input_tokens
        self.max_total_tokens = max_total_tokens
        self.temperature = temperature
        self.top_k = top_k
        self.top_p = top_p

        self.tokenizer = AutoTokenizer.from_pretrained(model_name_or_path)
    
    def prompt_fits(self, prompt_text):
        tokens = self.tokenizer(prompt_text, return_tensors="pt")
        return tokens.input_ids.shape[1] <= self.max_input_tokens
    
    '''def generate(self, prompt_text):
        if not self.prompt_fits(prompt_text):
            raise ValueError(f"Prompt exceeds the maximum input tokens ({self.max_input_tokens})")
        
        inputs = self.tokenizer(prompt_text, return_tensors="pt")
        outputs = self.model.generate(
            **inputs,
            max_new_tokens=self.max_total_tokens - inputs.input_ids.shape[1],
            temperature=self.temperature,
            top_k=self.top_k,
            top_p=self.top_p
        )
        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)'''