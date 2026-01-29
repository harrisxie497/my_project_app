from fastapi import APIRouter
from app.schemas.response import GeneralResponse

# 创建路由器
router = APIRouter(redirect_slashes=False)
admin_router = APIRouter(redirect_slashes=False)

# 测试路由
@router.get("", response_model=GeneralResponse[dict], tags=["test-config"])
async def test_config():
    return GeneralResponse(data={"message": "Test config route works!"})

# 管理员测试路由
@admin_router.get("", response_model=GeneralResponse[dict], tags=["admin-test-config"])
async def admin_test_config():
    return GeneralResponse(data={"message": "Admin test config route works!"})
