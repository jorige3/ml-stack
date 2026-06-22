from fastapi import FastAPI
from pydantic import BaseModel

from app.llm import generate
from app.memory import add, load

app = FastAPI(title="ChatGPT-like Local System")

class ChatRequest(BaseModel):
    prompt: str
    model: str = "qwen2.5-coder:1.5b"


@app.post("/chat")
def chat(req: ChatRequest):

    history = load()

    # simple prompt injection of memory
    context = "\n".join(
        [f"User: {h['user']}\nAssistant: {h['assistant']}" for h in history[-5:]]
    )

    full_prompt = f"""
You are a helpful assistant.

Conversation history:
{context}

User: {req.prompt}
Assistant:
"""

    result = generate(req.model, full_prompt)

    response_text = result.get("response", "")

    add(req.prompt, response_text)

    return {
        "response": response_text,
        "model": req.model
    }
