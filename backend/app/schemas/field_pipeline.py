from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class FieldPipelineBase(BaseModel):
    file_type: str = Field(..., description="文件类型", example="DELIVERY")
    target_col: str = Field(..., description="目标列", example="A")
    target_header: str = Field(..., description="目标表头", example="COL_A")
    map_op: str = Field(..., description="映射操作", example="COPY")
    source_cols: List[str] = Field(..., description="源列列表", example=["A"])
    field_type: str = Field(..., description="字段类型", example="FORMAT")
    rule_ref: List[str] = Field(..., description="规则引用", example=["fmt_date_yyyy_mm_dd"])
    depends_on: List[str] = Field(..., description="依赖列", example=[])
    order: int = Field(..., description="执行顺序", ge=1)
    enabled: bool = Field(True, description="启用状态")

class FieldPipelineCreate(FieldPipelineBase):
    pass

class FieldPipelineUpdate(BaseModel):
    file_type: Optional[str] = Field(None, description="文件类型")
    target_col: Optional[str] = Field(None, description="目标列")
    target_header: Optional[str] = Field(None, description="目标表头")
    map_op: Optional[str] = Field(None, description="映射操作")
    source_cols: Optional[List[str]] = Field(None, description="源列列表")
    field_type: Optional[str] = Field(None, description="字段类型")
    rule_ref: Optional[List[str]] = Field(None, description="规则引用")
    depends_on: Optional[List[str]] = Field(None, description="依赖列")
    order: Optional[int] = Field(None, description="执行顺序", ge=1)
    enabled: Optional[bool] = Field(None, description="启用状态")

class FieldPipelineResponse(FieldPipelineBase):
    id: str = Field(..., description="ID")
    created_at: datetime = Field(..., description="创建时间")
    updated_at: Optional[datetime] = Field(None, description="更新时间")
    
    class Config:
        from_attributes = True

class PaginatedFieldPipelineList(BaseModel):
    items: List[FieldPipelineResponse] = Field(..., description="字段映射列表")
    page: int = Field(..., description="页码", ge=1)
    page_size: int = Field(..., description="每页条数", ge=1)
    total: int = Field(..., description="总条数", ge=0)
