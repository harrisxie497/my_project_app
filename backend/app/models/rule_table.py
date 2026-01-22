from sqlalchemy import Column, String, Boolean, DateTime, Enum
from sqlalchemy.sql import func
from app.core.database import Base
import enum

# 规则阶段枚举
class RuleStage(str, enum.Enum):
    MAP = "MAP"
    PROCESS = "PROCESS"

# 文件类型枚举（复用task.py中的）
from app.models.task import FileType

# 规则表模型
class RuleTable(Base):
    __tablename__ = "rule_tables"
    
    id = Column(String(36), primary_key=True, index=True)
    code = Column(String(50), unique=True, index=True, nullable=False)
    name = Column(String(100), nullable=False)
    file_type = Column(Enum(FileType), nullable=False)
    rule_stage = Column(Enum(RuleStage), nullable=False)
    enabled = Column(Boolean, default=True, nullable=False)
    description = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
