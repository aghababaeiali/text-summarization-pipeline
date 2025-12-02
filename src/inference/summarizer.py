from pydoc import text
import time
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch
from src.utils.logging_utils import logger


class Summarizer:
    """
    Summarizer class that:
    - Loads tokenizer & model
    - Runs inference
    - Logs performance + device info
    """

    def __init__(
        self,
        model_path: str = "aliabbi/flan-t5-samsum-lora",
        max_length: int = 128,
        min_length: int = 30,
        temperature: float = 1.0,
        device: str = None,
    ):
        logger.info("Initializing Summarizer...")

        self.model_path = model_path
        self.max_length = max_length
        self.min_length = min_length
        self.temperature = temperature

        # Detect device
        self.device = device or (
            "cuda" if torch.cuda.is_available()
            else "mps" if torch.backends.mps.is_available()
            else "cpu"
        )

        logger.info(f"Using device: {self.device}")

        # Load tokenizer (slow tokenizer forced)
        start = time.time()
        logger.info(f"Loading tokenizer from {model_path}...")
        self.tokenizer = AutoTokenizer.from_pretrained(
            self.model_path,
            use_fast=False  # REQUIRED for T5 SentencePiece models
        )

        # Load model
        logger.info("Loading model...")
        self.model = AutoModelForSeq2SeqLM.from_pretrained(self.model_path)
        self.model.to(self.device)
        end = time.time()

        logger.info(
            f"Model + tokenizer loaded from {self.model_path} in {end - start:.2f}s"
        )

    def summarize(self, text: str):
        logger.info("Received summarize() request")

        if not text or not isinstance(text, str):
            logger.warning("Empty or invalid text input")
            raise ValueError("Text must be a non-empty string.")

        text = text.strip()
        if len(text) < 20:
            logger.warning(f"Text too short to summarize: {len(text)} chars")
            raise ValueError("Text too short to summarize (minimum 20 characters).")

        logger.info(f"Input length: {len(text)} characters")

        prompt = (
            "Summarize the conversation below.\n"
            "Your summary MUST follow these rules:\n"
            "- Do NOT add information that was not explicitly stated.\n"
            "- Do NOT infer intentions or future events.\n"
            "- ONLY describe facts mentioned in the dialogue.\n"
            "- Keep speakers' roles accurate.\n"
            "- Focus on the main points and outcomes.\n\n"
            "Conversation:\n"
            f"{text}\n\n"
            "Summary:"
        )



        # Tokenization
        logger.info("Tokenizing input...")
        t0 = time.time()
        inputs = self.tokenizer(
            prompt,
            return_tensors="pt",
            truncation=True,
            max_length=1024,
        ).to(self.device)
        t1 = time.time()
        logger.info(f"Tokenization complete in {(t1 - t0) * 1000:.2f} ms")

        # Generation
        logger.info("Generating summary...")
        outputs = self.model.generate(
            **inputs,
            max_length=self.max_length,
            min_length=self.min_length,
            num_beams=5,
            no_repeat_ngram_size=4,
            repetition_penalty=2.0,
            length_penalty=0.8,
            early_stopping=True,
            do_sample=False, 
        )
        t2 = time.time()
        logger.info(f"Generation complete in {(t2 - t1) * 1000:.2f} ms")

        summary = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        logger.info("Summary successfully generated")

        # Stats
        original_len = len(text)
        summary_len = len(summary)
        compression_ratio = summary_len / original_len

        logger.info(
            f"Summary stats — original: {original_len}, summary: {summary_len}, ratio: {compression_ratio:.2f}"
        )

        return {
            "summary": summary,
            "original_length": original_len,
            "summary_length": summary_len,
            "compression_ratio": compression_ratio,
            "tokenization_time": round((t1 - t0) * 1000, 2),
            "generation_time": round((t2 - t1) * 1000, 2),
            "total_time": round((t2 - t0) * 1000, 2),
        }
