from fastapi import APIRouter

router = APIRouter()

#Endpoint to verify the server is running
@router.get("/health")
async def health_check():
    return {"status": "ok"}