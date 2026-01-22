from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from app.models.task import FileType
from app.models.rule_item import OnFailStrategy

# AI字段能力基础模型
class AICapabilityBase(BaseModel):
    file_type: FileType = Field(..., description="文件类型")
    target_column: str = Field(..., description="目标列")
    target_field_name: str = Field(..., description="目标字段名称")
    capability_code: str = Field(..., description="能力编码")
    depends_on: List[str] = Field(..., description="依赖列列表")
    prompt_template: str = Field(..., description="提示模板")
    output_constraints_json: dict = Field(..., description="输出约束JSON")
    on_fail: OnFailStrategy = Field(default=OnFailStrategy.BLOCK, description="失败处理策略")
    enabled: bool = Field(default=True, description="是否启用")
    note: Optional[str] = Field(None, description="备注")

# 创建AI字段能力请求模型
class AICapabilityCreate(AICapabilityBase):
    pass

# 更新AI字段能力请求模型
class AICapabilityUpdate(BaseModel):
    target_field_name: Optional[str] = Field(None, description="目标字段名称")
    capability_code: Optional[str] = Field(None, description="能力编码")
    depends_on: Optional[List[str]] = Field(None, description="依赖列列表")
    prompt_template: Optional[str] = Field(None, description="提示模板")
    output_constraints_json: Optional[dict] = Field(None, description="输出约束JSON")
    on_fail: Optional[OnFailStrategy] = Field(None, description="失败处理策略")
    enabled: Optional[bool] = Field(None, description="是否启用")
    note: Optional[str] = Field(None, description="备注")

# AI字段能力响应模型
class AICapabilityResponse(BaseModel):
    id: str
    file_type: FileType
    target_column: str
    target_field_name: str
    capability_code: str
    depends_on: List[str]
    prompt_template: str
    output_constraints_json: dict
    on_fail: OnFailStrategy
    enabled: bool
    note: Optional[str]
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True

# 分页AI字段能力响应模型
class PaginatedAICapabilityList(BaseModel):
    items: list[AICapabilityResponse]
    page: int
    page_size: int
    total: int
