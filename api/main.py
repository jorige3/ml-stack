from fastapi import FastAPI
from pydantic import BaseModel
import requests
import os
import time
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI(title="ML Stack API")
Instrumentator().instrument(app).expose(app)

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://ollama:11434")

class GenerateRequest(BaseModel):
    prompt: str
    model: str = "qwen2.5-coder:1.5b"

@app.get("/")
def health():
    return {"status": "ok", "stack": "ml-ready"}

@app.get("/slow")
def slow():
    time.sleep(1)
    return {"status": "slow response complete"}

@app.post("/generate")
def generate(req: GenerateRequest):
    r = requests.post(
        f"{OLLAMA_HOST}/api/generate",
        json={
            "model": req.model,
            "prompt": req.prompt,
            "stream": False
        }
    )
    return r.json()
