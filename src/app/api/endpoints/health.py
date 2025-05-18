from fastapi import APIRouter, Depends
from typing import Dict
import httpx
from ...core.config import settings

router = APIRouter()

async def check_ollama() -> bool:
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{settings.OLLAMA_HOST}/api/health")
            return response.status_code == 200
    except:
        return False

async def check_qdrant() -> bool:
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"http://{settings.QDRANT_HOST}:{settings.QDRANT_PORT}/readyz")
            return response.status_code == 200
    except:
        return False

@router.get("/", response_model=Dict)
async def health_check():
    return {
        "status": "healthy",
        "services": {
            "ollama": "healthy" if await check_ollama() else "unhealthy",
            "qdrant": "healthy" if await check_qdrant() else "unhealthy",
            "redis": "healthy",  # Add Redis health check
            "n8n": "healthy"     # Add n8n health check
        }
    }
