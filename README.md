# 📝 Text Summarization Pipeline — FLAN-T5 + LoRA (Samsum)

A lightweight, production-ready **text summarization pipeline** built using:

- **FLAN-T5** fine-tuned on **Samsum** using **LoRA**
- **FastAPI** for serving inference via REST API  
- **Docker** for deployment  
- **Gradio** for a hosted interactive demo  
- **Hugging Face Hub** for model storage

🎉 **Live Demo (Gradio on Hugging Face):**  
https://huggingface.co/spaces/aliabbi/text-summarization-pipeline

---

## 🚀 Features

- Custom fine-tuned FLAN-T5 LoRA model  
- FastAPI endpoint for text summarization  
- Lightweight CPU-only Docker image  
- Clean & modular project structure  
- Logging utilities for debugging & performance tracking  
- Automated prompt prefixing to reduce speaker mix-ups  
- Gradio demo for recruiters to test instantly  

---

## 📁 Project Structure

```
text-summarization-pipeline/
│
├── api/
│   └── app.py                 # FastAPI server
│
├── data/
│   └── raw/                   # raw dataset (if needed)
│
├── models/
│   └── summarizer/            # exported fine-tuned model
│       ├── config.json
│       ├── model.safetensors
│       ├── tokenizer.json
│       └── ...
│
├── src/
│   ├── inference/
│   │   └── summarizer.py      # main summarization class
│   ├── training/
│   │   ├── dataset.py         # dataset handling
│   │   └── train.py           # LoRA training script
│   └── utils/
│       └── logging_utils.py   # shared logger
│
├── templates/
│   └── index.html             # FastAPI UI (optional)
│
├── tests/
│   └── test_api.py            # simple API test
│
├── Dockerfile
├── requirements.txt
├── upload_model.py
└── README.md
```

---

## 🎯 Model Training

- **Base model**: FLAN-T5-small  
- **LoRA fine-tuning** on **Samsum conversation summarization dataset**  
- **Platform used**: **Kaggle GPU**  
- **Training script**: `src/training/train.py`  
- **LoRA adapters merged** before exporting  
- Final model uploaded to Hugging Face:  
  **`aliabbi/flan-t5-samsum-lora`**

---

## 🧠 Inference Pipeline

The `Summarizer` class:

- Loads tokenizer + model only once (on CPU)
- Applies an engineered prompt prefix:
  > “Summarize the following conversation accurately. Do NOT mix up speakers. Preserve who said what.”
- Performs:
  - Tokenization  
  - Beam search decoding  
  - Summary generation  
  - Performance metrics logging  

---

## ⚡ FastAPI Usage

### **Run locally**
```bash
uvicorn api.app:app --reload
```

### **API Endpoint**
**POST** `/summarize`

**Request:**
```json
{
  "text": "Alex: Hey..."
}
```

**Response:**
```json
{
  "summary": "...",
  "original_length": 180,
  "summary_length": 58,
  "compression_ratio": 0.32
}
```

---

## 🐳 Docker Deployment

### **Build Image**
```bash
docker build -t summarizer .
```

### **Run Container**
```bash
docker run -p 8000:8000 summarizer
```

### **Dockerfile used**
```dockerfile
FROM python:3.10-slim

ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends     git     && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY api api
COPY src src
COPY templates templates

EXPOSE 8000

CMD ["uvicorn", "api.app:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## 📦 Requirements (FastAPI + Docker Version)

Exactly as used in your GitHub repo:

```txt
--extra-index-url https://download.pytorch.org/whl/cpu
torch==2.6.0+cpu
transformers==4.39.3
fastapi
uvicorn[standard]
jinja2
pydantic
numpy==1.26.4
huggingface_hub
python-multipart
sentencepiece
```

---

## 🌐 Hugging Face Space (Gradio) Version

The Gradio app is isolated from the Docker/REST version.  
It is lighter and easier to host on HF Spaces.

Requirements used:

```txt
gradio==4.44.0
huggingface_hub==0.23.2
transformers==4.39.3
torch==2.1.0
sentencepiece
accelerate
```

---

## 🎮 Gradio Demo (Local)

You may also run the Gradio app locally:

```bash
python app.py
```

This opens a local UI for testing summaries interactively.

---

## 📜 License

MIT — free to use for any purpose.
