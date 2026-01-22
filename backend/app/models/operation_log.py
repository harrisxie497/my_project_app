from sqlalchemy import Column, String, Boolean, DateTime, JSON
from sqlalchemy.sql import func
from app.core.database import Base

# 操作日志模型
class OperationLog(Base):
    __tablename__ = "operation_logs"
    
    id = Column(String(36), primary_key=True, index=True)
    user_id = Column(String(36), index=True, nullable=False)
    action = Column(String(50), index=True, nullable=False)  # 操作类型
    entity_type = Column(String(50), index=True, nullable=False)  # 实体类型
    entity_id = Column(String(36), index=True, nullable=True)  # 实体ID
    success = Column(Boolean, nullable=False, default=True)  # 是否成功
    message = Column(String(255), nullable=False)  # 操作消息
    detail_json = Column(JSON, nullable=True)  # 详细信息
    created_at = Column(DateTime(timezone=True), server_default=func.now())  # 操作时间
