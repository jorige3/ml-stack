import requests

OLLAMA_URL = "http://127.0.0.1:11434/api/generate"


def call_llm(
    message: str,
    history: list,
    context: str,
    model: str
):

    memory_context = "\n".join(
        f"User: {h['user']}\nAssistant: {h['assistant']}"
        for h in history
    )

    prompt = f"""
    You are a STRICT DOCUMENT-BASED AI.

    You must follow this hierarchy:

    1. Knowledge Base (highest priority)
    2. Conversation history
    3. General knowledge (ONLY if missing in KB)

    RULES:
    - If the Knowledge Base contains relevant info, USE ONLY IT.
    - Do NOT add extra explanations outside the docs.
    - If KB is empty, say: "I don't know from the provided documents."
    - Be concise.

    ====================
    KNOWLEDGE BASE
    ====================
    {context if context else "EMPTY"}

    ====================
    CONVERSATION
    ====================
    {memory_context}

    ====================
    USER QUESTION
    ====================
    {message}

    ====================
    FINAL ANSWER
    ====================
    """

    res = requests.post(
        OLLAMA_URL,
        json={
            "model": model,
            "prompt": prompt,
            "stream": False
        }
    )

    data = res.json()

    return data.get("response", "")