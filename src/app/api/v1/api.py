from fastapi import APIRouter

# Import your endpoint routers
from .endpoints import health, ai, vector, workflow

api_router = APIRouter()

# Include your routers
api_router.include_router(health.router, prefix="/health", tags=["health"])
api_router.include_router(ai.router, prefix="/ai", tags=["ai"])
api_router.include_router(vector.router, prefix="/vector", tags=["vector"])
api_router.include_router(workflow.router, prefix="/workflow", tags=["workflow"])