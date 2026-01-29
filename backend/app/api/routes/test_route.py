from fastapi import APIRouter
from app.schemas.response import GeneralResponse

router = APIRouter(redirect_slashes=False)

# 测试路由
@router.get("", response_model=GeneralResponse[dict], tags=["test"])
async def test_get():
    return GeneralResponse(data={"message": "Test GET route works!"})

@router.post("", response_model=GeneralResponse[dict], tags=["test"])
async def test_post():
    return GeneralResponse(data={"message": "Test POST route works!"})
