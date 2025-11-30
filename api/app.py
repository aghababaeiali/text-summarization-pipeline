from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.inference.summarizer import Summarizer

app = FastAPI(title="Text Summarization API")

# Load model at startup (later: local fine-tuned model)
summarizer = Summarizer()

class SummarizeRequest(BaseModel):
    text: str

class SummarizeResponse(BaseModel):
    summary: str
    compression_ratio: float
    original_length: int
    summary_length: int
    tokenization_time: float
    generation_time: float
    total_time: float


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/summarize", response_model=SummarizeResponse)
def summarize(request: SummarizeRequest):
    try:
        result = summarizer.summarize(request.text)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
