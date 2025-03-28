from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse, JSONResponse
from pydantic import BaseModel
from typing import Optional, AsyncGenerator
import asyncio
import json
import textwrap



router = APIRouter()

class ChatRequest(BaseModel):
    prompt: str
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


@router.post("/chat/stream")
async def stream_chat_response(request: Request):
    data = await request.json()
    prompt = data.get("prompt", "")
    rag = data.get("ragModel", "default")

    # Simulated metadata
    metadata = {
        "tokens_used": len(prompt.split()) + 10,
        "rag_model": rag,
        "source": "mock",
    }

    async def streamer():
        async for chunk in generate_stream_response(prompt):
            yield chunk

        # Send special JSON metadata token at end of stream
        yield "\n[END_METADATA] " + json.dumps(metadata)

    return StreamingResponse(streamer(), media_type="text/plain")

