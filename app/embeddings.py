import requests

OLLAMA_EMBED_URL = "http://127.0.0.1:11434/api/embeddings"
MODEL = "nomic-embed-text:latest"


def get_embedding(text: str):
    res = requests.post(
        OLLAMA_EMBED_URL,
        json={
            "model": MODEL,
            "prompt": text
        }
    )
    return res.json()["embedding"]
