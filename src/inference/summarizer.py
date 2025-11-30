import time
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch


class Summarizer:
    """
    Handles:
    - Loading the summarization model from local folder
    - Running inference
    - Returning summary + stats
    """

    def __init__(
        self,
        model_path: str = "google/flan-t5-small",
        max_length: int = 128,
        min_length: int = 30,
        temperature: float = 1.0,
        device: str = None,
    ):
        self.model_path = model_path
        self.max_length = max_length
        self.min_length = min_length
        self.temperature = temperature

        # Detect device
        self.device = device or ("cuda" if torch.cuda.is_available() else ("mps" if torch.backends.mps.is_available() else "cpu"))

        # Load tokenizer + model from local directory
        start = time.time()
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_path)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(self.model_path)
        self.model.to(self.device)
        end = time.time()

        print(f"[Summarizer] Loaded model from {self.model_path} on {self.device} in {end-start:.2f}s")

    def summarize(self, text: str):
        if not text or not isinstance(text, str):
            raise ValueError("Text must be a non-empty string.")

        text = text.strip()
        if len(text) < 20:
            raise ValueError("Text too short to summarize (minimum 20 characters).")

        # Tokenization
        t0 = time.time()
        inputs = self.tokenizer(
            text,
            return_tensors="pt",
            truncation=True,
            max_length=1024,
        ).to(self.device)
        t1 = time.time()

        # Generation
        outputs = self.model.generate(
            **inputs,
            max_length=self.max_length,
            min_length=self.min_length,
            temperature=self.temperature,
            do_sample=self.temperature > 1.0,
            num_beams=4,
        )
        t2 = time.time()

        summary = self.tokenizer.decode(outputs[0], skip_special_tokens=True)

        # Stats
        original_len = len(text)
        summary_len = len(summary)
        compression_ratio = summary_len / original_len

        return {
            "summary": summary,
            "original_length": original_len,
            "summary_length": summary_len,
            "compression_ratio": compression_ratio,
            "tokenization_time": round((t1 - t0) * 1000, 2),
            "generation_time": round((t2 - t1) * 1000, 2),
            "total_time": round((t2 - t0) * 1000, 2),
        }