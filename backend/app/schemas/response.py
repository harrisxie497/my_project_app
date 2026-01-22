from pydantic import BaseModel, Field
from typing import Optional, Generic, TypeVar

T = TypeVar('T')

# 错误响应模型
class ErrorResponse(BaseModel):
    code: str = Field(..., description="错误码")
    message: str = Field(..., description="错误消息")
    detail: Optional[dict] = Field(None, description="详细错误信息")

# 通用响应模型
class GeneralResponse(BaseModel, Generic[T]):
    ok: bool = Field(default=True, description="请求是否成功")
    data: Optional[T] = Field(None, description="响应数据")
    error: Optional[ErrorResponse] = Field(None, description="错误信息")
    
    class Config:
        from_attributes = True
