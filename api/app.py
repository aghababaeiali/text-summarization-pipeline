from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="text Summarization API")

class SummarizeRequest(BaseModel):
    text: str

class SummarizeResponse(BaseModel):
    summary: str
    compression_ratio: float
    original_length: int
    summary_length: int


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/summarize", response_model=SummarizeResponse)
def summarize(request: SummarizeRequest):
    """
    Temporary dummy implementation:
    - summary = first 100 characters
    - compression ratio = summary_len / original_len
    This will be replaced later with the real model.
    """
    original_text = request.text.strip()

    if not original_text:
        summary_text = ""
        original_len = 0
        summary_len = 0
        compression_ratio = 0.0
    else:
        original_len = len(original_text)
        summary_text = original_text[:100]
        summary_len = len(summary_text)
        compression_ratio = summary_len / original_len if original_len > 0 else 0.0

    return SummarizeResponse(
        summary=summary_text,
        compression_ratio=compression_ratio,
        original_length=original_len,
        summary_length=summary_len
    )
