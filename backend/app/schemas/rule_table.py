from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from app.models.rule_table import RuleStage, FileType

# 规则表基础模型
class RuleTableBase(BaseModel):
    code: str = Field(..., description="规则表编码")
    name: str = Field(..., description="规则表名称")
    file_type: FileType = Field(..., description="文件类型")
    rule_stage: RuleStage = Field(..., description="规则阶段")
    enabled: bool = Field(default=True, description="是否启用")
    description: Optional[str] = Field(None, description="规则表描述")

# 创建规则表请求模型
class RuleTableCreate(RuleTableBase):
    pass

# 更新规则表请求模型
class RuleTableUpdate(BaseModel):
    name: Optional[str] = Field(None, description="规则表名称")
    enabled: Optional[bool] = Field(None, description="是否启用")
    description: Optional[str] = Field(None, description="规则表描述")

# 规则表响应模型
class RuleTableResponse(BaseModel):
    id: str
    code: str
    name: str
    file_type: FileType
    rule_stage: RuleStage
    enabled: bool
    description: Optional[str]
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True

# 分页规则表响应模型
class PaginatedRuleTableList(BaseModel):
    items: list[RuleTableResponse]
    page: int
    page_size: int
    total: int
