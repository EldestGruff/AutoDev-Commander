from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Core
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    LOG_LEVEL: str = "INFO"

    # NVIDIA
    NVIDIA_VISIBLE_DEVICES: str = "all"
    CUDA_VERSION: str = "12.2"

    # Ollama
    OLLAMA_HOST: str = "http://ollama:11434"
    OLLAMA_MODEL: str = "llama2"

    # Qdrant
    QDRANT_HOST: str = "qdrant"
    QDRANT_PORT: int = 6333

    # Redis
    REDIS_URL: str = "redis://redis:6379/0"

    # n8n
    N8N_HOST: str = "localhost"
    N8N_PORT: int = 5678
    N8N_PROTOCOL: str = "http"

    class Config:
        env_file = ".env"

settings = Settings()
