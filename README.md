# RAGdio

Embed and query your documents.

## Example backend .env file

```
ASR_MODEL=whisper-api  # Options: whisper, whisper-api deepgram, huggingface, local
OPENAI_API_KEY=key
VECTOR_BACKEND=qdrant # Options: qdrant, chroma(in future)
EMBEDDING_BACKEND=huggingface   # Options: huggingface, openai
```
