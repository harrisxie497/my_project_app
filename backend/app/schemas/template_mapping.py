from pydantic import BaseModel, Field, field_validator
from typing import Optional, List, Dict, Any
from datetime import datetime
from app.models.template_mapping import SheetMatchMode
from app.models.task import FileType

# 模板映射基础模型
class TemplateMappingBase(BaseModel):
    mapping_code: str = Field(..., description="映射编码")
    file_type: FileType = Field(..., description="文件类型")
    source_template_code: str = Field(..., description="源模板编码")
    target_template_code: str = Field(..., description="目标模板编码")
    sheet_match_mode: SheetMatchMode = Field(..., description="Sheet匹配模式")
    sheet_match_value: str = Field(..., description="Sheet匹配值")
    column_bindings_json: dict = Field(..., description="列绑定JSON")
    enabled: bool = Field(default=True, description="是否启用")
    note: Optional[str] = Field(None, description="备注")

# 创建模板映射请求模型
class TemplateMappingCreate(TemplateMappingBase):
    pass

# 更新模板映射请求模型
class TemplateMappingUpdate(BaseModel):
    source_template_code: Optional[str] = Field(None, description="源模板编码")
    target_template_code: Optional[str] = Field(None, description="目标模板编码")
    sheet_match_mode: Optional[SheetMatchMode] = Field(None, description="Sheet匹配模式")
    sheet_match_value: Optional[str] = Field(None, description="Sheet匹配值")
    column_bindings_json: Optional[dict] = Field(None, description="列绑定JSON")
    enabled: Optional[bool] = Field(None, description="是否启用")
    note: Optional[str] = Field(None, description="备注")

# 模板映射响应模型
class TemplateMappingResponse(BaseModel):
    id: str
    mapping_code: str
    file_type: FileType
    source_template_code: str
    target_template_code: str
    sheet_match_mode: SheetMatchMode
    sheet_match_value: str
    column_bindings_json: dict
    enabled: bool
    note: Optional[str]
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True

# 分页模板映射响应模型
class PaginatedTemplateMappingList(BaseModel):
    items: list[TemplateMappingResponse]
    page: int
    page_size: int
    total: int
