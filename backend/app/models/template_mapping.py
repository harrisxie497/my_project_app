from sqlalchemy import Column, String, Boolean, DateTime, JSON, Enum
from sqlalchemy.sql import func
from app.core.database import Base
import enum

# 文件类型枚举（复用task.py中的）
from app.models.task import FileType

# Sheet匹配模式枚举
class SheetMatchMode(str, enum.Enum):
    NAME = "name"
    INDEX = "index"

# 模板映射模型
class TemplateMapping(Base):
    __tablename__ = "template_mappings"
    
    id = Column(String(36), primary_key=True, index=True)
    mapping_code = Column(String(50), unique=True, index=True, nullable=False)
    file_type = Column(Enum(FileType), nullable=False)
    source_template_code = Column(String(50), nullable=False)
    target_template_code = Column(String(50), nullable=False)
    sheet_match_mode = Column(Enum(SheetMatchMode), nullable=False)
    sheet_match_value = Column(String(50), nullable=False)
    column_bindings_json = Column(JSON, nullable=False)
    enabled = Column(Boolean, default=True, nullable=False)
    note = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
