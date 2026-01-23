from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from uuid import uuid4
import os
from datetime import datetime
from typing import Optional, List
from app.core.auth import get_current_active_user
from app.core.config import settings
from app.core.database import get_db
from app.models.user import User
from app.models.task import Task, TaskStatus, FileType
from app.schemas.task import (
    TaskCreate, TaskRun, TaskListResponse, TaskDetailResponse,
    TaskCreateResponse, PaginatedTaskList
)
from app.schemas.response import GeneralResponse

router = APIRouter(redirect_slashes=False)

# 创建任务（上传文件）
@router.post("", response_model=GeneralResponse[TaskCreateResponse], tags=["tasks"])
async def create_task(
    file_type: str = Form(...),
    unique_code: str = Form(...),
    flight_no: Optional[str] = Form(None),
    declare_date: Optional[str] = Form(None),
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    # 验证文件类型
    if not file.filename.endswith(".xlsx"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only .xlsx files are allowed"
        )
    
    # 验证必填字段
    file_type_enum = FileType(file_type)
    if file_type_enum == FileType.CUSTOMS:
        if not flight_no:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="flight_no is required for customs file type"
            )
        if not declare_date:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="declare_date is required for customs file type"
            )
    
    # 生成任务ID
    task_id = f"t_{uuid4().hex[:8]}"
    
    # 创建任务记录
    task = Task(
        id=task_id,
        created_by_user_id=current_user.id,
        file_type=file_type_enum,
        unique_code=unique_code,
        flight_no=flight_no,
        declare_date=declare_date,
        status=TaskStatus.QUEUED,
        files={}
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    
    # 创建任务文件存储目录
    task_dir = os.path.join(settings.TASKS_STORAGE_PATH, task_id)
    os.makedirs(task_dir, exist_ok=True)
    
    # 保存上传的文件
    file_path = os.path.join(task_dir, "original.xlsx")
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())
    
    # 更新任务文件信息
    task.files = {
        "original": {
            "file_name": file.filename,
            "download_url": f"{settings.API_V1_STR}/tasks/{task_id}/files/original"
        }
    }
    db.commit()
    
    return GeneralResponse(
        data=TaskCreateResponse(
            task_id=task.id,
            status=task.status
        )
    )

# 运行任务
@router.post("/{task_id}/run", response_model=GeneralResponse[TaskCreateResponse], tags=["tasks"])
async def run_task(
    task_id: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    # 获取任务，检查用户权限
    task = db.query(Task).filter(
        Task.id == task_id,
        Task.created_by_user_id == current_user.id
    ).first()
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    
    # 验证任务状态
    if task.status in [TaskStatus.SUCCESS, TaskStatus.FAILED]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot run a task that has already completed or failed"
        )
    
    # 更新任务状态为处理中
    task.status = TaskStatus.PROCESSING
    task.started_at = datetime.utcnow()
    task.progress_stage = "processing"
    task.progress_message = "Task is running"
    db.commit()
    
    try:
            # 获取任务文件存储目录
            task_dir = os.path.join(settings.TASKS_STORAGE_PATH, task_id)
            
            # 导入文件处理器
            from app.services.file_processor import FileProcessor
            
            # 创建文件处理器实例，并传递数据库会话
            processor = FileProcessor(task_dir, task.file_type.value, db)
            
            # 执行文件处理
            stats = processor.process()
            
            # 更新任务的文件信息
            task.files.update({
                "result": {
                    "file_name": f"result_{task.id}.xlsx",
                    "download_url": f"{settings.API_V1_STR}/tasks/{task_id}/files/result"
                },
                "diff": {
                    "file_name": f"diff_{task.id}.xlsx",
                    "download_url": f"{settings.API_V1_STR}/tasks/{task_id}/files/diff"
                }
            })
            
            # 更新任务统计信息
            task.stats = stats
            
            # 更新任务状态为成功
            task.status = TaskStatus.SUCCESS
            task.finished_at = datetime.utcnow()
            task.progress_stage = "done"
            task.progress_message = "Task completed successfully"
            
            db.commit()
        
    except Exception as e:
        # 更新任务状态为失败
        task.status = TaskStatus.FAILED
        task.finished_at = datetime.utcnow()
        task.progress_stage = "failed"
        task.progress_message = f"Task failed: {str(e)}"
        db.commit()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Task failed: {str(e)}"
        )
    
    return GeneralResponse(
        data=TaskCreateResponse(
            task_id=task.id,
            status=task.status
        )
    )

# 获取任务列表
@router.get("", response_model=GeneralResponse[PaginatedTaskList], tags=["tasks"])
async def get_tasks(
    file_type: Optional[str] = None,
    status: Optional[str] = None,
    unique_code: Optional[str] = None,
    page: int = 1,
    page_size: int = 20,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    # 构建查询
    query = db.query(Task).filter(Task.created_by_user_id == current_user.id)
    
    # 应用过滤条件
    if file_type:
        query = query.filter(Task.file_type == FileType(file_type))
    if status:
        query = query.filter(Task.status == TaskStatus(status))
    if unique_code:
        query = query.filter(Task.unique_code.contains(unique_code))
    
    # 计算总数
    total = query.count()
    
    # 应用分页
    skip = (page - 1) * page_size
    tasks = query.order_by(Task.created_at.desc()).offset(skip).limit(page_size).all()
    
    # 转换为响应模型
    task_list = [TaskListResponse.from_orm(task) for task in tasks]
    
    return GeneralResponse(
        data=PaginatedTaskList(
            items=task_list,
            page=page,
            page_size=page_size,
            total=total
        )
    )

# 获取任务详情
@router.get("/{task_id}", response_model=GeneralResponse[TaskDetailResponse], tags=["tasks"])
async def get_task_detail(
    task_id: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    # 获取任务
    task = db.query(Task).filter(
        Task.id == task_id,
        Task.created_by_user_id == current_user.id
    ).first()
    
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    
    return GeneralResponse(data=TaskDetailResponse.from_orm(task))

# 下载任务文件
@router.get("/{task_id}/files/{file_kind}", tags=["tasks"])
async def download_task_file(
    task_id: str,
    file_kind: str,  # original, result, diff
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    # 获取任务
    task = db.query(Task).filter(
        Task.id == task_id,
        Task.created_by_user_id == current_user.id
    ).first()
    
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    
    # 验证文件类型
    if file_kind not in ["original", "result", "diff"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid file kind"
        )
    
    # 验证文件是否存在
    task_dir = os.path.join(settings.TASKS_STORAGE_PATH, task_id)
    file_path = os.path.join(task_dir, f"{file_kind}.xlsx")
    
    if not os.path.exists(file_path):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found"
        )
    
    # 返回文件
    from fastapi.responses import FileResponse
    return FileResponse(
        path=file_path,
        filename=task.files.get(file_kind, {}).get("file_name", f"{file_kind}.xlsx"),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
