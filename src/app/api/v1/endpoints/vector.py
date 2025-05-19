from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def vector_root():
    return {"message": "Vector endpoints"}