from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from loguru import logger

from .core.logger import setup_logging
from .core.config import settings
from .core.di import get_container
from .api.v1.api import api_router

setup_logging()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    container = get_container()
    app.state.container = container
    logger.info("Starting AutoDev Commander...")
    
    yield
    
    # Shutdown
    if hasattr(app.state, "container"):
        await app.state.container.cleanup()
    logger.info("Shutting down AutoDev Commander...")

app = FastAPI(
    title="AutoDev Commander",
    description="AI-Driven Development Orchestration",
    version="0.1.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api/v1")

# Add a simple health check
@app.get("/health")
async def health_check():
    return {"status": "healthy"}