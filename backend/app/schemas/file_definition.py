from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from datetime import datetime

class FileDefinitionBase(BaseModel):
    file_type: str = Field(..., description="文件类型", example="DELIVERY")
    file_role: str = Field(..., description="文件角色", example="source")
    sheet_name: str = Field(..., description="工作表名称", example="Delivery")
    header_row: int = Field(1, description="表头行", ge=1)
    data_start_row: int = Field(2, description="数据起始行", ge=1)
    columns_json: List[Dict[str, str]] = Field(..., description="列定义", example=[{"col": "A", "header": "COL_A"}])
    enabled: bool = Field(True, description="启用状态")

class FileDefinitionCreate(FileDefinitionBase):
    pass

class FileDefinitionUpdate(BaseModel):
    file_type: Optional[str] = Field(None, description="文件类型")
    file_role: Optional[str] = Field(None, description="文件角色")
    sheet_name: Optional[str] = Field(None, description="工作表名称")
    header_row: Optional[int] = Field(None, description="表头行", ge=1)
    data_start_row: Optional[int] = Field(None, description="数据起始行", ge=1)
    columns_json: Optional[List[Dict[str, str]]] = Field(None, description="列定义")
    enabled: Optional[bool] = Field(None, description="启用状态")

class FileDefinitionResponse(FileDefinitionBase):
    id: str = Field(..., description="ID")
    created_at: datetime = Field(..., description="创建时间")
    updated_at: Optional[datetime] = Field(None, description="更新时间")
    
    class Config:
        from_attributes = True

class PaginatedFileDefinitionList(BaseModel):
    items: List[FileDefinitionResponse] = Field(..., description="文件定义列表")
    page: int = Field(..., description="页码", ge=1)
    page_size: int = Field(..., description="每页条数", ge=1)
    total: int = Field(..., description="总条数", ge=0)
