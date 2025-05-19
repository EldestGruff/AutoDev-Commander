from fastapi import APIRouter, Depends
from ....core.di import get_ollama_service, get_qdrant_service, get_n8n_service

router = APIRouter()

@router.get("/system-check")
async def system_check(
    ollama=Depends(get_ollama_service),
    qdrant=Depends(get_qdrant_service),
    n8n=Depends(get_n8n_service)
):
    """Test all service connections"""
    status = {
        "ollama": "unknown",
        "qdrant": "unknown",
        "n8n": "unknown"
    }
    
    try:
        # Test Ollama
        await ollama.get_embedding("test")
        status["ollama"] = "connected"
    except Exception as e:
        status["ollama"] = f"error: {str(e)}"

    try:
        # Test Qdrant
        await qdrant.create_collection("test_collection")
        status["qdrant"] = "connected"
    except Exception as e:
        status["qdrant"] = f"error: {str(e)}"

    try:
        # Test n8n
        await n8n.get_workflow_status("test")
        status["n8n"] = "connected"
    except Exception as e:
        status["n8n"] = f"error: {str(e)}"

    return status
