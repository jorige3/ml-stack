import json
from pathlib import Path

DB = Path("data/chats.json")
DB.parent.mkdir(exist_ok=True)

def load():
    if not DB.exists():
        return []
    return json.loads(DB.read_text())

def save(messages):
    DB.write_text(json.dumps(messages, indent=2))

def add(user: str, assistant: str):
    history = load()
    history.append({"user": user, "assistant": assistant})
    save(history)
