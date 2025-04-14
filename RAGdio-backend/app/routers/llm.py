from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse, JSONResponse
from pydantic import BaseModel
from typing import Optional, AsyncGenerator

import asyncio
import json
import uuid
import textwrap

from app.services.rag_pipeline import RAGPipelineService

router = APIRouter()

class ChatRequest(BaseModel):
    prompt: str
    chat_id: Optional[str] = None
    ragModel: Optional[str] = "default"

class ChatResponse(BaseModel):
    response: str
    metadata: Optional[dict] = None

# Simulate word-by-word async response (mocking LLM stream)
async def generate_stream_response(prompt: str) -> AsyncGenerator[str, None]:
    text = textwrap.dedent(f"""
    ## Hello!

    Here's a Python example:

    ```python
    def hello():
        print("Hello world!")
    ```

    Let me know if you need anything else.
    """).strip()
    for line in text.splitlines():
        yield line + "\n"
        await asyncio.sleep(0.05)


@router.post("/chat/stream/test")
async def stream_chat_response(request: Request):
    data = await request.json()
    prompt = data.get("prompt", "")
    rag = data.get("ragModel", "default") # feature: some particular collection

    # Simulated metadata
    metadata = {
        "tokens_used": len(prompt.split()) + 10, # TODO maybe some proper calc?
        "rag_model": rag,
        "source": "mock",
    }

    async def streamer():
        async for chunk in generate_stream_response(prompt):
            yield chunk

        # Send special JSON metadata token at end of stream
        yield "\n[END_METADATA] " + json.dumps(metadata)

    return StreamingResponse(streamer(), media_type="text/plain")




pipeline = RAGPipelineService()



from app.services.chat_memory import (
    append_turn, build_prompt, get_chat_context,auto_summarize
)
from app.core.config import Config


@router.post("/chat/stream")
async def stream_chat_response(payload: ChatRequest):
    chat_id = payload.chat_id or str(uuid.uuid4())
    prompt = payload.prompt

    append_turn(chat_id, "user", prompt)
    full_prompt = build_prompt(chat_id, prompt)
    
    rag_result = pipeline.query(full_prompt)
    answer = rag_result["answer"]
    sources = rag_result.get("context_docs", [])

    append_turn(chat_id, "assistant", answer)
    auto_summarize(chat_id)

    async def streamer():
        yield answer + "\n"
        await asyncio.sleep(0.01)

        context = get_chat_context(chat_id)
        # Convert deque to list for JSON serialization
        serializable_context = {
            "turns": list(context["turns"]),
            "summary": context["summary"],
            "context": context["context"],
            "chat_id": chat_id,
            "sources": sources,
        }

        yield "\n[END_METADATA] " + json.dumps(serializable_context)

    return StreamingResponse(streamer(), media_type="text/plain")