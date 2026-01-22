from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from app.models.rule_item import MapOp, FieldType, ExecutorType, OnFailStrategy

# 规则项基础模型
class RuleItemBase(BaseModel):
    enabled: bool = Field(default=True, description="是否启用")
    order_no: int = Field(default=10, description="执行顺序")
    target_column: str = Field(..., description="目标列")
    target_field_name: str = Field(..., description="目标字段名称")
    map_op: Optional[MapOp] = Field(None, description="映射操作")
    source_column: Optional[str] = Field(None, description="源列")
    field_type: Optional[FieldType] = Field(None, description="字段类型")
    process_depends_on: Optional[str] = Field(None, description="处理依赖")
    process_rules_json: Optional[dict] = Field(None, description="处理规则JSON")
    executor: Optional[ExecutorType] = Field(None, description="执行器")
    on_fail: OnFailStrategy = Field(default=OnFailStrategy.BLOCK, description="失败处理策略")
    note: Optional[str] = Field(None, description="备注")

# 创建规则项请求模型
class RuleItemCreate(RuleItemBase):
    rule_table_id: str = Field(..., description="规则表ID")

# 更新规则项请求模型
class RuleItemUpdate(BaseModel):
    enabled: Optional[bool] = Field(None, description="是否启用")
    order_no: Optional[int] = Field(None, description="执行顺序")
    target_column: Optional[str] = Field(None, description="目标列")
    target_field_name: Optional[str] = Field(None, description="目标字段名称")
    map_op: Optional[MapOp] = Field(None, description="映射操作")
    source_column: Optional[str] = Field(None, description="源列")
    field_type: Optional[FieldType] = Field(None, description="字段类型")
    process_depends_on: Optional[str] = Field(None, description="处理依赖")
    process_rules_json: Optional[dict] = Field(None, description="处理规则JSON")
    executor: Optional[ExecutorType] = Field(None, description="执行器")
    on_fail: Optional[OnFailStrategy] = Field(None, description="失败处理策略")
    note: Optional[str] = Field(None, description="备注")

# 规则项响应模型
class RuleItemResponse(BaseModel):
    id: str
    rule_table_id: str
    enabled: bool
    order_no: int
    target_column: str
    target_field_name: str
    map_op: Optional[MapOp]
    source_column: Optional[str]
    field_type: Optional[FieldType]
    process_depends_on: Optional[str]
    process_rules_json: Optional[dict]
    executor: Optional[ExecutorType]
    on_fail: OnFailStrategy
    note: Optional[str]
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True

# 分页规则项响应模型
class PaginatedRuleItemList(BaseModel):
    items: list[RuleItemResponse]
    page: int
    page_size: int
    total: int
