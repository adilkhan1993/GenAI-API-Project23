import os
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from dotenv import load_dotenv

load_dotenv()

class ModelInference:
    def __init__(self):
        self.model = None
        self.tokenizer = None
        # Для простоты и скорости оставляем gpt2, чтобы сервер в облаке легко запустился
        self.model_path = os.getenv("MODEL_PATH", "gpt2") 

    def load_model(self):
        print(f"Загрузка модели из {self.model_path}...")
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_path)
        
        device_map = "auto" if torch.cuda.is_available() else "cpu"
        
        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_path,
            device_map=device_map,
            torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32
        )
        print("✅ Модель успешно загружена!")

    def generate(self, prompt: str, max_tokens: int) -> tuple[str, int]:
        if not self.model or not self.tokenizer:
            raise RuntimeError("Модель не загружена")
            
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.model.device)
        
        outputs = self.model.generate(
            **inputs,
            max_new_tokens=max_tokens,
            temperature=0.7,
            do_sample=True,
            pad_token_id=self.tokenizer.eos_token_id
        )
        
        # Считаем, сколько новых токенов сгенерировалось
        generated_ids = outputs[0][inputs.input_ids.shape[1]:]
        generated_text = self.tokenizer.decode(generated_ids, skip_special_tokens=True)
        
        return generated_text.strip(), len(generated_ids)

inference_engine = ModelInference()