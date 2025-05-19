from typing import Dict, Any
from fastapi import Depends
from functools import lru_cache

from ..services.ai.ollama_service import OllamaService
from ..services.vector.qdrant_service import QdrantService
from ..services.workflow.n8n_service import N8NService

class ServiceContainer:
    def __init__(self):
        self._services: Dict[str, Any] = {}
        self.init_services()

    def init_services(self):
        self._services = {
            "ollama": OllamaService(),
            "qdrant": QdrantService(),
            "n8n": N8NService(),
        }

    @property
    def ollama(self) -> OllamaService:
        return self._services["ollama"]

    @property
    def qdrant(self) -> QdrantService:
        return self._services["qdrant"]

    @property
    def n8n(self) -> N8NService:
        return self._services["n8n"]

@lru_cache()
def get_container() -> ServiceContainer:
    return ServiceContainer()

def get_ollama_service(
    container: ServiceContainer = Depends(get_container)
) -> OllamaService:
    return container.ollama

def get_qdrant_service(
    container: ServiceContainer = Depends(get_container)
) -> QdrantService:
    return container.qdrant

def get_n8n_service(
    container: ServiceContainer = Depends(get_container)
) -> N8NService:
    return container.n8n
