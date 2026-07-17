from fastapi import FastAPI
import logging
import os

from app.schemas import ChatRequest
from app.llm import call_llm
from app.memory import save_chat, get_history
from app.stream import router as stream_router
from app.rag import retrieve_context, build_index

app = FastAPI(title="ML Stack ChatGPT Clone")

# include streaming router
app.include_router(stream_router)

# logging setup
logger = logging.getLogger("ml-stack")
logging.basicConfig(level=logging.INFO)


@app.on_event("startup")
def startup_event():
    build_index()


@app.post("/chat")
def chat(req: ChatRequest):
    # 1. Load memory
    history = get_history(req.session_id)

    # 2. RAG retrieval
    doc_context = retrieve_context(query=req.message)

    # 3. Log safely
    logger.info("RAG context used: %s", doc_context)

    # 4. Call LLM
    response = call_llm(
        message=req.message,
        history=history,
        context=doc_context,
        model=req.model
    )

    # 5. Save memory
    save_chat(req.session_id, req.message, response)

    # 6. Return response
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
