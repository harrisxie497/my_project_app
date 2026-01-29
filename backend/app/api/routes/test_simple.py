from fastapi import APIRouter

router = APIRouter()

@router.get("/test", tags=["test"])
async def test():
    return {"message": "Test route works!"}
