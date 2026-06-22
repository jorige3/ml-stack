import requests

OLLAMA_URL = "http://127.0.0.1:11434/api/generate"


def call_llm(message: str, history: list, model: str):

    # simple prompt builder
    context = "\n".join(
        [f"User: {h['user']}\nAssistant: {h['assistant']}" for h in history]
    )

    prompt = f"""
You are a helpful assistant.

Conversation history:
{context}

User:
{message}

Answer:
"""

    res = requests.post(
        OLLAMA_URL,
        json={
            "model": model,
            "prompt": prompt,
            "stream": False
        }
    )

    return res.json()["response"]