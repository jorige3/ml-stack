from fastapi import APIRouter
from fastapi.responses import StreamingResponse
import requests
import json

router = APIRouter()

OLLAMA_URL = "http://127.0.0.1:11434/api/generate"

def generate_stream(prompt: str, model: str):
    response = requests.post(
        OLLAMA_URL,
        json={
            "model": model,
            "prompt": prompt,
            "stream": True
        },
        stream=True
    )

    for line in response.iter_lines():
        if line:
            data = json.loads(line.decode("utf-8"))
            if "response" in data:
                yield data["response"]

@router.post("/chat/stream")
def chat_stream(payload: dict):
    prompt = payload["message"]
    model = payload.get("model", "qwen2.5-coder:1.5b")

    return StreamingResponse(
        generate_stream(prompt, model),
        media_type="text/plain"
    )