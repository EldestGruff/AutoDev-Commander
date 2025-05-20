from typing import List, Optional
import httpx
from loguru import logger
from pydantic import BaseModel

from ...core.config import settings
from ...core.exceptions import (
    AIServiceError,
    ModelNotLoadedError,
    EmbeddingError,
    GenerationError,
    ServiceConnectionError
)

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
        if not text:
            raise ValidationError("Text cannot be empty")
            
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
            except httpx.HTTPStatusError as e:
                if e.response.status_code == 404:
                    raise ModelNotLoadedError(self.model)
                raise EmbeddingError(f"Failed to get embedding: {str(e)}")
            except httpx.RequestError as e:
                raise ServiceConnectionError("Ollama", str(e))
            except Exception as e:
                logger.error(f"Unexpected error getting embedding: {e}")
                raise AIServiceError(f"Unexpected error: {str(e)}")

    async def generate_text(self, prompt: str, **kwargs) -> str:
        """Generate text using Ollama."""
        if not prompt:
            raise ValidationError("Prompt cannot be empty")
            
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
            except httpx.HTTPStatusError as e:
                if e.response.status_code == 404:
                    raise ModelNotLoadedError(self.model)
                raise GenerationError(f"Failed to generate text: {str(e)}")
            except httpx.RequestError as e:
                raise ServiceConnectionError("Ollama", str(e))
            except Exception as e:
                logger.error(f"Unexpected error generating text: {e}")
                raise AIServiceError(f"Unexpected error: {str(e)}")