from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from ...services.vector.qdrant_service import QdrantService

router = APIRouter()
qdrant_service = QdrantService()

class VectorUpsertRequest(BaseModel):
    collection_name: str
    vectors: List[List[float]]
    payloads: List[Dict[str, Any]]
    ids: Optional[List[str]] = None

class VectorSearchRequest(BaseModel):
    collection_name: str
    query_vector: List[float]
    limit: int = 5

@router.post("/collections/{collection_name}")
async def create_collection(
    collection_name: str,
    vector_size: int = 768
):
    try:
        await qdrant_service.create_collection(collection_name, vector_size)
        return {"status": "success", "message": f"Collection {collection_name} created"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/vectors/upsert")
async def upsert_vectors(request: VectorUpsertRequest):
    try:
        await qdrant_service.upsert_vectors(
            request.collection_name,
            request.vectors,
            request.payloads,
            request.ids
        )
        return {"status": "success", "message": "Vectors upserted"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/vectors/search")
async def search_vectors(request: VectorSearchRequest):
    try:
        results = await qdrant_service.search_vectors(
            request.collection_name,
            request.query_vector,
            request.limit
        )
        return {"results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
