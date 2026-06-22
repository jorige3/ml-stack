import requests

EMBED_URL = "http://127.0.0.1:11434/api/embeddings"

def embed(text: str):
    r = requests.post(
        EMBED_URL,
        json={
            "model": "nomic-embed-text:latest",
            "prompt": text
        }
    )
    return r.json()["embedding"]
