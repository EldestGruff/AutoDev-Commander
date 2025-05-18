from typing import List, Optional
import httpx
from loguru import logger
from pydantic import BaseModel

from ...core.config import settings

class EmbeddingRequest(BaseModel):
    model: str
    prompt: str
    options: Optional[dict] = None

class EmbeddingResponse(BaseModel):
    embedding: List[float]

class OllamaService:
    def __init__(self):
        self.base_url = settings.OLLAMA_HOST
        self.model = settings.OLLAMA_MODEL

    async def get_embedding(self, text: str) -> List[float]:
        """Get embeddings for text using Ollama."""
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    f"{self.base_url}/api/embeddings",
                    json={
                        "model": self.model,
                        "prompt": text
                    }
                )
                response.raise_for_status()
                data = response.json()
                return data["embedding"]
            except Exception as e:
                logger.error(f"Error getting embedding: {e}")
                raise

    async def generate_text(self, prompt: str, **kwargs) -> str:
        """Generate text using Ollama."""
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    f"{self.base_url}/api/generate",
                    json={
                        "model": self.model,
                        "prompt": prompt,
                        **kwargs
                    }
                )
                response.raise_for_status()
                data = response.json()
                return data["response"]
            except Exception as e:
                logger.error(f"Error generating text: {e}")
                raise
