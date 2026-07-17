import json
# load_memory removed - not needed

DATA_PATH = "data/chats.json"


def retrieve_context(session_id: str, query: str):
    memory = get_history()

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

def build_index(doc_dir: str = "data/docs", index_path: str = "data/doc_index.json"):
    """Build document index from files in doc_dir and save to index_path"""
    import json
    from pathlib import Path
    from datetime import datetime
    
    documents = []
    doc_dir = Path(doc_dir)
    
    for file_path in doc_dir.glob("*"):
        if file_path.is_file():
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
                documents.append({
                    "path": str(file_path),
                    "content": content
                })
    
    index = {
        "documents": documents,
        "created_at": datetime.now().isoformat()
    }
    
    with open(index_path, "w", encoding="utf-8") as f:
        json.dump(index, f)
    
    print(f"Built index with {len(documents)} documents")
    return index
