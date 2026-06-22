from fastapi import FastAPI

from app.schemas import ChatRequest
from app.llm import call_llm
from app.memory import save_chat, get_history

from app.stream import router as stream_router

app = FastAPI(title="ML Stack ChatGPT Clone")

# only include streaming router for now
app.include_router(stream_router)


@app.post("/chat")
def chat(req: ChatRequest):

    history = get_history(req.session_id)

    response = call_llm(
        message=req.message,
        history=history,
        model=req.model
    )

    save_chat(req.session_id, req.message, response)

    return {
        "session_id": req.session_id,
        "response": response,
        "history": history + [
            {
                "user": req.message,
                "assistant": response
            }
        ]
    }