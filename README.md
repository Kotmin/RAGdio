# 🎧 RAGdio – Audio-First RAG with Local + Cloud AI

**RAGdio** is an audio-focused RAG (Retrieval-Augmented Generation) framework combining transcription, semantic search, and multiple LLM backends — both local and cloud-based.

> 💡 Built with clean code, adapters, interfaces, and a minimal full-stack (FastAPI + Vite).


<p align="center">
  <img 
    src="./docs/media/rag_mem_short.gif" 
    alt="query RAG + memory" 
    width="80%" 
    style="border-radius: 8px;" 
  />
</p>


### 🧪 Current Status

> **RAGdio is intended for local use, testing, and development purposes.**  
> It's not production-ready and not designed for multi-user environments (yet).

- ❗ Great for **experimenting** with audio-to-RAG pipelines locally.
- ⚙️ Designed with **modularity** in mind — adapters, interfaces, and clean architecture.
- 🚫 Not optimized for production load, scaling, or secure multi-user handling.
- 📌 Requires manual setup of models (e.g., in Ollama) after first run.

---

Chat with memory/history feature (available in API and Local models)

### ✅ Check transcription before add to RAG
<p align="center">
  <img 
    src="./docs/media/add_element_to_rag_p1_v3.gif" 
    alt="Check provided transcription" 
    width="80%" 
    style="border-radius: 8px;" 
  />
</p>

### 🔍 Query
<p align="center">
  <img 
    src="./docs/media/add_element_to_rag_p2.gif" 
    alt="Query RAG" 
    width="80%" 
    style="border-radius: 8px;" 
  />
</p>

---

## 🚀 Quick Start (with Docker)

```bash
git clone https://github.com/Kotmin/RAGdio
cd RAGdio

# 1. Configure environment variables
copy from examples or manually set up

# 2. Start services
docker compose up --build
```


Once everything is up and running, you can access:

- 🖥️ **Frontend**: [http://localhost:5173](http://localhost:5173)  
- 📡 **Backend (API docs)**: [http://localhost:8000/docs](http://localhost:8000/docs)

### ⚠️ Note (Ollama Users)
The default `docker-compose` setup includes an **Ollama server** _without any model pre-installed_.  
After running `docker compose up`, you must install a model manually.

You can install **Zephyr** or any other supported model.  
👉 See [**Scenario 1: Ollama + Zephyr (lightweight local)**](#-scenario-1-ollama--zephyr-lightweight-local) for model installation instructions.


Then open:

- **Frontend**: http://localhost:5173
- **Backend** (API docs): http://localhost:8000/docs
- if using ollama: `install model` ()

---

## ⚙️ .env Example (`RAGdio-backend/.env`)

```env
ASR_MODEL=whisper                  # whisper, whisper-api
OPENAI_API_KEY=sk-...              # for OpenAI-based features

VECTOR_BACKEND=qdrant             # qdrant
QDRANT_HOST=qdrant                # if starded within docker 
EMBEDDING_BACKEND=huggingface     # huggingface, openai

LLM_PROVIDER_TYPE=ollama          # openai, ollama, deepseek, local
LLM_RAG_MODE=rag_fallback         # rag_fallback, rag_strict

LOCAL_OLLM_MODEL=zephyr
LOCAL_OLLM_API_URL=http://localhost:11434/api/generate

DEBUG=true
```

### LLM RAG MODES (if available)

- "rag_strict" – LLM can only answer from documents

- "rag_fallback" – If docs are not useful or missing, LLM falls back to its own knowledge


## ⚙️ .env Example (`rag-audio-frontend.env`)

```env
VITE_API_BASE_URL=http://localhost:8000/api
```

## VITE_API_BASE_URL=http://localhost:8000/api

## 📦 Supported ASR + LLM Backends

| Component     | Options                                 |
| ------------- | --------------------------------------- |
| Transcription | `whisper`, `whisper-api`                |
| Embeddings    | `huggingface`, `openai`                 |
| Vector DB     | `qdrant` (with Docker)                  |
| LLM Backends  | `openai`, `ollama`, `deepseek`, `local` |

---

## 🧠 LLM RAG Modes

| Mode           | Description                                                                 |
| -------------- | --------------------------------------------------------------------------- |
| `rag_strict`   | LLM must only answer using provided documents                               |
| `rag_fallback` | LLM can fallback to its own knowledge if context is unclear or insufficient |

---

## 📼 Audio Transcription

**Supported formats**:

```
mp3, mp4, mpeg, mpga, m4a, wav, webm
```

We recommend `whisper` with `"medium"` or higher model for best local accuracy.

---

## 🧪 Test Scenarios

### ✅ Scenario 1: Ollama + Zephyr (lightweight local)
* Zephyr can be replaced with any llm

#### Requirements

- ~3.5 GB disk (Zephyr model)
- 7 GB RAM
- ~1 GB VRAM (optional)

#### Setup

```bash
docker exec -it ollama ollama pull zephyr
```

.env:

```env
LLM_PROVIDER_TYPE=ollama
LOCAL_OLLM_MODEL=zephyr
```

#### Flow

1. Upload 3 audio files (MP3/WAV/WEBM/etc.)
2. Transcribe + ingest to RAG
3. Ask a contextual question (e.g. "What did Krzysio say?")
4. Ask general question (e.g. "What's the capital of Poland?")
5. Ask "What was my previous question?" (test memory)

---

### ✅ Scenario 2: DeepSeek LLM (local, 7B)

#### Requirements

- ~13–15 GB disk
- 8–16 GB RAM
- GPU highly recommended

#### Setup

.env:

```env
LLM_PROVIDER_TYPE=deepseek
```

Model downloads automatically via `transformers`.

Same test flow as Scenario 1.

---

### ✅ Scenario 3: Fully Remote (OpenAI)

.env:

```env
ASR_MODEL=whisper-api
OPENAI_API_KEY=sk-...
VECTOR_BACKEND=qdrant
QDRANT_HOST=qdrant
EMBEDDING_BACKEND=openai
LLM_PROVIDER_TYPE=openai
LLM_RAG_MODE=rag_fallback
```

No local models needed. Ideal for low-resource devices.

---

## 🧠 Chat Memory & Context

- Stored in `chat_id` (browser localStorage)
- Up to 10-turn rolling memory (user + assistant)
- Injected as summary/context for compatible models
- Shared to LLM as part of prompt (unless using OpenAI’s own chain)

Sample structure:

```json
{
  "chat_id": "uuid...",
  "turns": [ { "role": "user", "content": "..." }, ... ],
  "summary": "optional summary",
  "context": "optional injected context"
}
```

---

## 💾 System Requirements

| Stack              | Disk Usage | RAM     | VRAM    |
| ------------------ | ---------- | ------- | ------- |
| `ollama + zephyr`  | ~3.5 GB    | ~3 GB   | ~1 GB   |
| `deepseek-7b-chat` | ~13–15 GB  | 8–16 GB | ~10 GB  |
| `OpenAI (API)`     | None       | ~500 MB | None    |
| `Whisper (medium)` | ~2 GB      | ~2–3 GB | ~1–2 GB |
| `Qdrant`           | ~300 MB    | ~300 MB | None    |

---

## 🏗 Architecture

- 🧠 **Langchain** for RAG + chaining
- 🗃 **Qdrant** as vector DB (via Docker)
- 🧱 Clean adapter-based architecture (LLM, ASR, Embeddings)
- 🎙 Whisper for audio transcription
- 🌐 FastAPI backend + Vite frontend

---

## 🛠 Development Reference

```bash
# Run full app
docker compose up --build

# Access frontend
http://localhost:5173

# Access backend (API docs)
http://localhost:8000/docs

# Pull Zephyr model (inside container)
docker exec -it ollama ollama pull zephyr
```

---

## 📁 Project Structure (Simplified)

```
RAGdio/
├── RAGdio-backend/
│   ├── app/
│   │   ├── adapters/         # LLM, audio, embedding adapters
│   │   ├── services/         # RAG pipeline, chat memory
│   │   ├── routers/          # FastAPI routes
│   │   └── core/             # Config, logging
├── rag-audio-frontend/       # React + Tailwind UI
├── docker-compose.yml
```

---

## 📃 License

MIT License. Built to tinker, break, and rebuild — have fun with audio-first RAG!
