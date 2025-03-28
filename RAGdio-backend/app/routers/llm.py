from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()

class ChatRequest(BaseModel):
    prompt: str
    ragModel: str | None = "default"

class ChatResponse(BaseModel):
    response: str
    metadata: dict | None = None

@router.post("/chat", response_model=ChatResponse)
async def chat_with_llm(request: ChatRequest):
    try:
        # Simple echo behavior for mock
        return ChatResponse(
            response=f"🧠 [mocked] You said: {request.prompt}",
            metadata={
                "model_used": request.ragModel,
                "tokens": len(request.prompt.split()),
                "source": "mock/llm"
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
