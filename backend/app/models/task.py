from sqlalchemy import Column, String, DateTime, Enum, JSON, Integer
from sqlalchemy.sql import func
from app.core.database import Base
import enum

# 任务状态枚举
class TaskStatus(str, enum.Enum):
    QUEUED = "queued"
    PROCESSING = "processing"
    SUCCESS = "success"
    FAILED = "failed"

# 文件类型枚举
class FileType(str, enum.Enum):
    CUSTOMS = "customs"
    DELIVERY = "delivery"

# 任务模型
class Task(Base):
    __tablename__ = "tasks"
    
    id = Column(String(36), primary_key=True, index=True)
    created_by_user_id = Column(String(36), nullable=False)
    file_type = Column(Enum(FileType), nullable=False)
    unique_code = Column(String(100), nullable=False)
    flight_no = Column(String(20), nullable=True)
    declare_date = Column(String(10), nullable=True)  # YYYY-MM-DD
    status = Column(Enum(TaskStatus), default=TaskStatus.QUEUED, nullable=False)
    progress_stage = Column(String(50), nullable=True)
    progress_message = Column(String(255), nullable=True)
    error = Column(JSON, nullable=True)
    stats = Column(JSON, nullable=True)
    files = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    started_at = Column(DateTime(timezone=True), nullable=True)
    finished_at = Column(DateTime(timezone=True), nullable=True)
