import json
from app.memory import load_memory

DATA_PATH = "data/chats.json"


def retrieve_context(session_id: str, query: str):
    memory = load_memory()

    history = memory.get(session_id, [])

    # simple baseline RAG (we’ll upgrade to embeddings later)
    last_messages = history[-5:]

    return last_messages


def build_prompt(context, user_message: str):
    formatted = ""

    for item in context:
        formatted += f"User: {item['user']}\nAssistant: {item['assistant']}\n"

    formatted += f"\nUser: {user_message}\nAssistant:"

    return formatted