from sqlalchemy import Column, String, Boolean, DateTime, JSON, Enum, ARRAY
from sqlalchemy.sql import func
from app.core.database import Base
import enum

# 文件类型枚举（复用task.py中的）
from app.models.task import FileType

# 失败处理策略枚举（复用rule_item.py中的）
from app.models.rule_item import OnFailStrategy

# AI字段能力模型
class AICapability(Base):
    __tablename__ = "ai_capabilities"
    
    id = Column(String(36), primary_key=True, index=True)
    file_type = Column(Enum(FileType), nullable=False)
    target_column = Column(String(10), nullable=False)
    target_field_name = Column(String(100), nullable=False)
    capability_code = Column(String(50), nullable=False)
    depends_on = Column(JSON, nullable=False)  # 依赖列列表
    prompt_template = Column(String(500), nullable=False)
    output_constraints_json = Column(JSON, nullable=False)
    on_fail = Column(Enum(OnFailStrategy), nullable=False, default=OnFailStrategy.BLOCK)
    enabled = Column(Boolean, default=True, nullable=False)
    note = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
