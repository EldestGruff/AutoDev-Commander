from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from ...services.ai.ollama_service import OllamaService

router = APIRouter()
ollama_service = OllamaService()

class EmbeddingRequest(BaseModel):
    text: str

class EmbeddingResponse(BaseModel):
    embedding: List[float]

class GenerateRequest(BaseModel):
    prompt: str
    options: Optional[dict] = None

class GenerateResponse(BaseModel):
    text: str

@router.post("/embed", response_model=EmbeddingResponse)
async def create_embedding(request: EmbeddingRequest):
    try:
        embedding = await ollama_service.get_embedding(request.text)
        return {"embedding": embedding}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/generate", response_model=GenerateResponse)
async def generate_text(request: GenerateRequest):
    try:
        text = await ollama_service.generate_text(
            request.prompt,
            **(request.options or {})
        )
        return {"text": text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
