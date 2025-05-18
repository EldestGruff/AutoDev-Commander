from fastapi import APIRouter
from .endpoints import ai, vector, workflow, health

api_router = APIRouter()

api_router.include_router(health.router, prefix="/health", tags=["health"])
api_router.include_router(ai.router, prefix="/ai", tags=["ai"])
api_router.include_router(vector.router, prefix="/vector", tags=["vector"])
api_router.include_router(workflow.router, prefix="/workflow", tags=["workflow"])
