from sqlalchemy import Column, String, Boolean, Integer, DateTime, JSON, Enum
from sqlalchemy.sql import func
from app.core.database import Base
import enum

# 映射操作枚举
class MapOp(str, enum.Enum):
    COPY = "COPY"
    DROP = "DROP"
    DERIVE = "DERIVE"

# 字段类型枚举
class FieldType(str, enum.Enum):
    RULE_FIX = "RULE_FIX"
    CALC = "CALC"
    AI = "AI"

# 执行器类型枚举
class ExecutorType(str, enum.Enum):
    PROGRAM = "program"
    AI = "ai"
    OTHER_PROGRAM = "other_program"

# 失败处理策略枚举
class OnFailStrategy(str, enum.Enum):
    BLOCK = "block"
    SKIP = "skip"
    USE_DEFAULT = "use_default"

# 规则项模型
class RuleItem(Base):
    __tablename__ = "rule_items"
    
    id = Column(String(36), primary_key=True, index=True)
    rule_table_id = Column(String(36), index=True, nullable=False)
    enabled = Column(Boolean, default=True, nullable=False)
    order_no = Column(Integer, nullable=False, default=10)
    target_column = Column(String(10), nullable=False)
    target_field_name = Column(String(100), nullable=False)
    map_op = Column(Enum(MapOp), nullable=True)
    source_column = Column(String(10), nullable=True)
    field_type = Column(Enum(FieldType), nullable=True)
    process_depends_on = Column(String(255), nullable=True)
    process_rules_json = Column(JSON, nullable=True)
    executor = Column(Enum(ExecutorType), nullable=True)
    on_fail = Column(Enum(OnFailStrategy), nullable=True, default=OnFailStrategy.BLOCK)
    note = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
