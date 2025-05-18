from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from .core.logger import setup_logging
from .core.config import settings

setup_logging()

app = FastAPI(
    title="AutoDev Commander",
    description="AI-Driven Development Orchestration",
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    logger.info("Starting AutoDev Commander...")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down AutoDev Commander...")

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "environment": settings.ENVIRONMENT,
        "services": {
            "ollama": "operational",
            "qdrant": "operational",
            "redis": "operational",
            "n8n": "operational"
        }
    }
