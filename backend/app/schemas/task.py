from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum

# 文件类型枚举
class FileType(str, Enum):
    CUSTOMS = "customs"
    DELIVERY = "delivery"

# 任务状态枚举
class TaskStatus(str, Enum):
    QUEUED = "queued"
    PROCESSING = "processing"
    SUCCESS = "success"
    FAILED = "failed"

# 任务创建请求
class TaskCreate(BaseModel):
    file_type: FileType
    unique_code: str = Field(..., min_length=1, max_length=100)
    flight_no: Optional[str] = Field(None, max_length=20)
    declare_date: Optional[str] = Field(None, pattern="^\d{4}-\d{2}-\d{2}$")

# 任务运行请求
class TaskRun(BaseModel):
    pass

# 任务统计信息
class TaskStats(BaseModel):
    total_rows: Optional[int] = None
    fixed_count: Optional[int] = None
    filled_count: Optional[int] = None
    fx_changed_rows: Optional[int] = None
    llm_filled_count: Optional[int] = None

# 任务文件信息
class TaskFile(BaseModel):
    file_name: str
    download_url: str

# 任务文件列表
class TaskFiles(BaseModel):
    original: Optional[TaskFile] = None
    result: Optional[TaskFile] = None
    diff: Optional[TaskFile] = None

# 任务错误信息
class TaskError(BaseModel):
    code: str
    message: str
    detail: Optional[dict] = None

# 任务响应基础信息
class TaskBase(BaseModel):
    id: str
    file_type: FileType
    unique_code: str
    status: TaskStatus
    created_at: datetime

# 任务列表响应
class TaskListResponse(TaskBase):
    flight_no: Optional[str] = None
    declare_date: Optional[str] = None
    started_at: Optional[datetime] = None
    finished_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

# 任务详情响应
class TaskDetailResponse(TaskListResponse):
    created_by_user_id: str
    progress_stage: Optional[str] = None
    progress_message: Optional[str] = None
    error: Optional[TaskError] = None
    stats: Optional[TaskStats] = None
    files: Optional[TaskFiles] = None
    
    class Config:
        from_attributes = True

# 任务创建响应
class TaskCreateResponse(BaseModel):
    task_id: str
    status: TaskStatus

# 分页任务列表响应
class PaginatedTaskList(BaseModel):
    items: List[TaskListResponse]
    page: int
    page_size: int
    total: int
