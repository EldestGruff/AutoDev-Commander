from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def workflow_root():
    return {"message": "Workflow endpoints"}