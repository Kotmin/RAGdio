# RAGdio

Embed and query your documents.

## Example backend .env file

```
ASR_MODEL=whisper-api  # Options: whisper, whisper-api, (in future) deepgram, huggingface, local
OPENAI_API_KEY=key
VECTOR_BACKEND=qdrant # Options: qdrant, chroma(in future)
EMBEDDING_BACKEND=huggingface   # Options: huggingface, openai
LLM_PROVIDER_TYPE=openai # Options openai,ollama,deepseek,local
LLM_RAG_MODE=rag_fallback  # rag_fallback or rag_strict
LOCAL_OLLM_API_URL=
LOCAL_OLLM_MODEL=zephyr
```

## LLM RAG MODES (if available)

- "rag_strict" – LLM can only answer from documents

- "rag_fallback" – If docs are not useful or missing, LLM falls back to its own knowledge


## Run local ollama Zephyr
```bash
docker exec -it ollama ollama pull zephyr
```
Inside docker compose we have ollama instance, we can