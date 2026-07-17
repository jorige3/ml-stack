# ml-stack

FastAPI-based Retrieval-Augmented Generation (RAG) service combining BM25 and semantic retrieval with local LLM inference via Ollama.

**Tech stack:**
- FastAPI (API)
- SQLAlchemy (data / metadata)
- Ollama (local LLM inference)
- Hybrid retrieval: BM25 + semantic (FAISS)
- Monitoring: Prometheus + Grafana (docker-compose)

## Prerequisites
- Python 3.11+
- Ollama running (Windows host or WSL2-native) and reachable from the app

## Setup

1. Install dependencies:

```bash
uv sync
```

2. Configure the Ollama URL in `.env`:
On WSL2, this should be your Windows host's gateway IP, not `127.0.0.1` — find it with:
```bash
ip route show default
```

If `OLLAMA_URL` is unset, `app/config.py` auto-detects the WSL2 gateway IP as a fallback.

## Runtime

Run the app with Uvicorn (recommended sync workers for local inference):

```bash
uv run uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## Notes
- The codebase expects Ollama endpoints for generation and embeddings (see `app/llm.py` and `app/embeddings.py`).
- Use synchronous Uvicorn workers when calling local Ollama to avoid concurrency issues with model inference.

## Docker Compose: monitoring

The repository includes a `docker-compose.yml` that starts `prometheus` and `grafana` alongside an `api` service. To run the monitoring stack only:

```bash
docker compose up prometheus grafana
```

## Access
- API: http://localhost:8000
- Grafana: http://localhost:3000 (default admin/admin)
- Prometheus: http://localhost:9090

## License
See project files for licensing.
