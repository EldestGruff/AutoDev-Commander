from typing import Dict, Any, Optional
from functools import lru_cache
from pydantic import BaseModel
from fastapi import Depends

class ServiceConfig(BaseModel):
    """Configuration for services"""
    ollama_url: str
    qdrant_host: str
    qdrant_port: int
    n8n_url: str
    redis_url: str

class DependencyContainer:
    """Central dependency injection container"""
    def __init__(self, config: ServiceConfig):
        self.config = config
        self._services: Dict[str, Any] = {}
        
    @property
    def ollama(self):
        if 'ollama' not in self._services:
            from ..services.ai.ollama_service import OllamaService
            self._services['ollama'] = OllamaService(
                base_url=self.config.ollama_url
            )
        return self._services['ollama']
    
    @property
    def qdrant(self):
        if 'qdrant' not in self._services:
            from ..services.vector.qdrant_service import QdrantService
            self._services['qdrant'] = QdrantService(
                host=self.config.qdrant_host,
                port=self.config.qdrant_port
            )
        return self._services['qdrant']
    
    @property
    def n8n(self):
        if 'n8n' not in self._services:
            from ..services.workflow.n8n_service import N8NService
            self._services['n8n'] = N8NService(
                base_url=self.config.n8n_url
            )
        return self._services['n8n']

    async def cleanup(self):
        """Cleanup services on shutdown"""
        for service in self._services.values():
            if hasattr(service, 'cleanup'):
                await service.cleanup()

@lru_cache()
def get_container() -> DependencyContainer:
    """Get or create dependency container"""
    from .config import settings
    config = ServiceConfig(
        ollama_url=settings.OLLAMA_HOST,
        qdrant_host=settings.QDRANT_HOST,
        qdrant_port=settings.QDRANT_PORT,
        n8n_url=f"{settings.N8N_PROTOCOL}://{settings.N8N_HOST}:{settings.N8N_PORT}",
        redis_url=settings.REDIS_URL
    )
    return DependencyContainer(config)

# Service dependency getters
def get_ollama_service(container: DependencyContainer = Depends(get_container)):
    return container.ollama

def get_qdrant_service(container: DependencyContainer = Depends(get_container)):
    return container.qdrant

def get_n8n_service(container: DependencyContainer = Depends(get_container)):
    return container.n8n
