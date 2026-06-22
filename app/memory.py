import json
from pathlib import Path

DB_PATH = Path("data/chats.json")


def _load():
    if DB_PATH.exists():
        return json.loads(DB_PATH.read_text())
    return {}


def _save(data):
    DB_PATH.write_text(json.dumps(data, indent=2))


def get_history(session_id: str):
    data = _load()
    return data.get(session_id, [])


def save_chat(session_id: str, user_message: str, assistant_response: str):
    data = _load()

    if session_id not in data:
        data[session_id] = []

    history = data[session_id]

    new_entry = {
        "user": user_message,
        "assistant": assistant_response
    }

    # 🚨 prevent duplicate consecutive entries
    if history and history[-1] == new_entry:
        return

    history.append(new_entry)

    # keep last N turns
    data[session_id] = history[-20:]

    _save(data)