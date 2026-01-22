from sqlalchemy import Column, String, Boolean, DateTime, JSON, Enum
from sqlalchemy.sql import func
from app.core.database import Base
import enum

# 文件类型枚举（复用task.py中的）
from app.models.task import FileType

# Excel配置模型
class ExcelConfig(Base):
    __tablename__ = "excel_configs"
    
    id = Column(String(36), primary_key=True, index=True)
    file_type = Column(Enum(FileType), nullable=False)
    default_font = Column(String(50), nullable=False, default="Meiryo")
    date_format = Column(String(20), nullable=False, default="YYYY-MM-DD")
    merge_ranges = Column(JSON, nullable=False, default=[])
    style_rules = Column(JSON, nullable=False, default=[])
    enabled = Column(Boolean, default=True, nullable=False)
    is_active = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
