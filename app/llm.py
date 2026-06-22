import requests

OLLAMA_URL = "http://127.0.0.1:11434/api/generate"

def generate(model: str, prompt: str, stream: bool = False):
    r = requests.post(
        OLLAMA_URL,
        json={
            "model": model,
            "prompt": prompt,
            "stream": stream
        },
        timeout=120
    )
    r.raise_for_status()
    return r.json()
