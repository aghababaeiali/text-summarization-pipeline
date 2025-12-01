from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from src.inference.summarizer import Summarizer
from src.utils.logging_utils import logger


app = FastAPI(title="Text Summarization API")

logger.info("🚀 Starting Text Summarization API...")

# Load templates
templates = Jinja2Templates(directory="templates")

# Load ML model at startup
logger.info("📥 Loading Summarizer model at startup...")
summarizer = Summarizer()
logger.info("✅ Model loaded successfully")


# -------------------------------
# Pydantic request/response models
# -------------------------------

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


# -------------------------------
# ROUTES
# -------------------------------

@app.get("/", response_class=HTMLResponse)
def ui(request: Request):
    logger.info("📄 UI page requested")
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/health")
def health_check():
    logger.info("🔍 Health check requested")
    return {"status": "ok"}


@app.post("/summarize", response_model=SummarizeResponse)
def summarize(request: SummarizeRequest):
    logger.info(f"📝 /summarize called — Input length: {len(request.text)} chars")

    try:
        result = summarizer.summarize(request.text)
        logger.info("✅ Summary generated successfully")
        return result

    except Exception as e:
        logger.error(f"❌ Error during summarization: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
