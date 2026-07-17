import faiss
import numpy as np
import json
from pathlib import Path
from app.embeddings import get_embedding

DOCS_DIR = Path("data/docs")

INDEX_FILE = "data/faiss.index"
META_FILE = "data/faiss_meta.json"

dimension = 768  # nomic-embed-text embedding size (important)

index = faiss.IndexFlatIP(dimension)
metadata = []


def normalize(vec):
    v = np.array(vec).astype("float32")
    return v / np.linalg.norm(v)


def build_index():
    global index, metadata

    if Path(INDEX_FILE).exists():
        index = faiss.read_index(INDEX_FILE)
        metadata = json.loads(Path(META_FILE).read_text())
        return

    vectors = []
    metadata = []

    for file in DOCS_DIR.glob("*.txt"):
        content = file.read_text(encoding="utf-8")

        emb = normalize(get_embedding(content))

        vectors.append(emb)
        metadata.append({
            "name": file.name,
            "content": content
        })

    vectors = np.array(vectors).astype("float32")

    index.add(vectors)

    faiss.write_index(index, INDEX_FILE)
    Path(META_FILE).write_text(json.dumps(metadata))
