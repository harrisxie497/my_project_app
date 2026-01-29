from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime

class RuleDefinitionBase(BaseModel):
    rule_ref: str = Field(..., description="规则引用", example="fmt_date_yyyy_mm_dd")
    rule_type: str = Field(..., description="规则类型", example="FORMAT")
    executor_type: str = Field(..., description="执行器类型", example="program")
    schema_json: Dict[str, Any] = Field(..., description="规则参数Schema", example={"type": "object", "properties": {"output_format": {"type": "string"}}})
    enabled: bool = Field(True, description="启用状态")

class RuleDefinitionCreate(RuleDefinitionBase):
    pass

class RuleDefinitionUpdate(BaseModel):
    rule_type: Optional[str] = Field(None, description="规则类型")
    executor_type: Optional[str] = Field(None, description="执行器类型")
    schema_json: Optional[Dict[str, Any]] = Field(None, description="规则参数Schema")
    enabled: Optional[bool] = Field(None, description="启用状态")

class RuleDefinitionResponse(RuleDefinitionBase):
    created_at: datetime = Field(..., description="创建时间")
    updated_at: Optional[datetime] = Field(None, description="更新时间")
    
    class Config:
        from_attributes = True

class PaginatedRuleDefinitionList(BaseModel):
    items: list[RuleDefinitionResponse] = Field(..., description="规则定义列表")
    page: int = Field(..., description="页码", ge=1)
    page_size: int = Field(..., description="每页条数", ge=1)
    total: int = Field(..., description="总条数", ge=0)
