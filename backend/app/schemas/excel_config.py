from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from app.models.task import FileType

# Excel配置基础模型
class ExcelConfigBase(BaseModel):
    file_type: FileType = Field(..., description="文件类型")
    default_font: str = Field(default="Meiryo", description="默认字体")
    date_format: str = Field(default="YYYY-MM-DD", description="日期格式")
    merge_ranges: List[str] = Field(default=[], description="合并区域列表")
    style_rules: List[dict] = Field(default=[], description="样式规则列表")
    enabled: bool = Field(default=True, description="是否启用")

# 创建Excel配置请求模型
class ExcelConfigCreate(ExcelConfigBase):
    pass

# 更新Excel配置请求模型
class ExcelConfigUpdate(BaseModel):
    default_font: Optional[str] = Field(None, description="默认字体")
    date_format: Optional[str] = Field(None, description="日期格式")
    merge_ranges: Optional[List[str]] = Field(None, description="合并区域列表")
    style_rules: Optional[List[dict]] = Field(None, description="样式规则列表")
    enabled: Optional[bool] = Field(None, description="是否启用")

# Excel配置响应模型
class ExcelConfigResponse(BaseModel):
    id: str
    file_type: FileType
    default_font: str
    date_format: str
    merge_ranges: List[str]
    style_rules: List[dict]
    enabled: bool
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True

# 分页Excel配置响应模型
class PaginatedExcelConfigList(BaseModel):
    items: list[ExcelConfigResponse]
    page: int
    page_size: int
    total: int
