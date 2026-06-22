from pydantic import BaseModel


class ChatRequest(BaseModel):
    message: str
    session_id: str
    model: str = "qwen2.5-coder:1.5b"