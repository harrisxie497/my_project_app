from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

# 操作日志基础模型
class OperationLogBase(BaseModel):
    user_id: str = Field(..., description="用户ID")
    action: str = Field(..., description="操作类型")
    entity_type: str = Field(..., description="实体类型")
    entity_id: Optional[str] = Field(None, description="实体ID")
    success: bool = Field(default=True, description="是否成功")
    message: str = Field(..., description="操作消息")
    detail_json: Optional[Dict[str, Any]] = Field(None, description="详细信息")

# 创建操作日志请求模型
class OperationLogCreate(OperationLogBase):
    pass

# 操作日志响应模型
class OperationLogResponse(BaseModel):
    id: str
    user_id: str
    action: str
    entity_type: str
    entity_id: Optional[str]
    success: bool
    message: str
    detail_json: Optional[Dict[str, Any]]
    created_at: datetime
    
    class Config:
        from_attributes = True

# 分页操作日志列表响应
class PaginatedOperationLogList(BaseModel):
    items: List[OperationLogResponse]
    page: int
    page_size: int
    total: int
