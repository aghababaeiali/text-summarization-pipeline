from fastapi.testclient import TestClient
from api.pp import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_summarize_dummy():
    payload = {"text": "This is a long text that will be summarized by our API in a dummy way for now."}
    response = client.post("/summarize", json=payload)
    data = response.json()
    assert "summary" in data
    assert "compression_ratio" in data

