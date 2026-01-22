from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from uuid import uuid4
from typing import Optional, List
from datetime import datetime
from app.core.auth import get_current_active_user
from app.core.config import settings
from app.core.database import get_db
from app.models.user import User
from app.models.operation_log import OperationLog
from app.schemas.operation_log import (
    OperationLogCreate, OperationLogResponse, PaginatedOperationLogList
)
from app.schemas.response import GeneralResponse

router = APIRouter(redirect_slashes=False)
admin_router = APIRouter(redirect_slashes=False)

# 获取操作日志列表
@router.get("", response_model=GeneralResponse[PaginatedOperationLogList], tags=["operation-logs"])
async def get_operation_logs(
    user_id: Optional[str] = Query(None, description="用户ID过滤"),
    action: Optional[str] = Query(None, description="操作类型过滤"),
    entity_type: Optional[str] = Query(None, description="实体类型过滤"),
    entity_id: Optional[str] = Query(None, description="实体ID过滤"),
    success: Optional[bool] = Query(None, description="是否成功过滤"),
    from_time: Optional[datetime] = Query(None, description="开始时间过滤"),
    to_time: Optional[datetime] = Query(None, description="结束时间过滤"),
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页条数"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    # 构建查询
    query = db.query(OperationLog)
    
    # 应用过滤条件
    if user_id:
        query = query.filter(OperationLog.user_id == user_id)
    if action:
        query = query.filter(OperationLog.action == action)
    if entity_type:
        query = query.filter(OperationLog.entity_type == entity_type)
    if entity_id:
        query = query.filter(OperationLog.entity_id == entity_id)
    if success is not None:
        query = query.filter(OperationLog.success == success)
    if from_time:
        query = query.filter(OperationLog.created_at >= from_time)
    if to_time:
        query = query.filter(OperationLog.created_at <= to_time)
    
    # 计算总数
    total = query.count()
    
    # 应用分页
    skip = (page - 1) * page_size
    operation_logs = query.order_by(OperationLog.created_at.desc()).offset(skip).limit(page_size).all()
    
    # 转换为响应模型
    operation_log_list = [OperationLogResponse.from_orm(log) for log in operation_logs]
    
    return GeneralResponse(
        data=PaginatedOperationLogList(
            items=operation_log_list,
            page=page,
            page_size=page_size,
            total=total
        )
    )

# 获取操作日志详情
@router.get("/{id}", response_model=GeneralResponse[OperationLogResponse], tags=["operation-logs"])
async def get_operation_log(
    id: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    operation_log = db.query(OperationLog).filter(OperationLog.id == id).first()
    if not operation_log:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Operation log with id '{id}' not found"
        )
    
    return GeneralResponse(data=OperationLogResponse.from_orm(operation_log))

# 获取指定用户的操作日志
@router.get("/user/{user_id}", response_model=GeneralResponse[List[OperationLogResponse]], tags=["operation-logs"])
async def get_operation_logs_by_user(
    user_id: str,
    action: Optional[str] = Query(None, description="操作类型过滤"),
    success: Optional[bool] = Query(None, description="是否成功过滤"),
    from_time: Optional[datetime] = Query(None, description="开始时间过滤"),
    to_time: Optional[datetime] = Query(None, description="结束时间过滤"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    # 构建查询
    query = db.query(OperationLog).filter(OperationLog.user_id == user_id)
    
    # 应用过滤条件
    if action:
        query = query.filter(OperationLog.action == action)
    if success is not None:
        query = query.filter(OperationLog.success == success)
    if from_time:
        query = query.filter(OperationLog.created_at >= from_time)
    if to_time:
        query = query.filter(OperationLog.created_at <= to_time)
    
    # 获取操作日志
    operation_logs = query.order_by(OperationLog.created_at.desc()).all()
    
    # 转换为响应模型
    operation_log_list = [OperationLogResponse.from_orm(log) for log in operation_logs]
    
    return GeneralResponse(data=operation_log_list)

# 获取指定操作的日志
@router.get("/action/{action}", response_model=GeneralResponse[List[OperationLogResponse]], tags=["operation-logs"])
async def get_operation_logs_by_action(
    action: str,
    user_id: Optional[str] = Query(None, description="用户ID过滤"),
    success: Optional[bool] = Query(None, description="是否成功过滤"),
    from_time: Optional[datetime] = Query(None, description="开始时间过滤"),
    to_time: Optional[datetime] = Query(None, description="结束时间过滤"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    # 构建查询
    query = db.query(OperationLog).filter(OperationLog.action == action)
    
    # 应用过滤条件
    if user_id:
        query = query.filter(OperationLog.user_id == user_id)
    if success is not None:
        query = query.filter(OperationLog.success == success)
    if from_time:
        query = query.filter(OperationLog.created_at >= from_time)
    if to_time:
        query = query.filter(OperationLog.created_at <= to_time)
    
    # 获取操作日志
    operation_logs = query.order_by(OperationLog.created_at.desc()).all()
    
    # 转换为响应模型
    operation_log_list = [OperationLogResponse.from_orm(log) for log in operation_logs]
    
    return GeneralResponse(data=operation_log_list)

# 管理员查询操作日志
@admin_router.get("", response_model=GeneralResponse[PaginatedOperationLogList], tags=["admin-operation-logs"])
async def admin_get_operation_logs(
    user_id: Optional[str] = Query(None, description="用户ID过滤"),
    action: Optional[str] = Query(None, description="操作类型过滤"),
    entity_type: Optional[str] = Query(None, description="实体类型过滤"),
    entity_id: Optional[str] = Query(None, description="实体ID过滤"),
    success: Optional[bool] = Query(None, description="是否成功过滤"),
    from_time: Optional[datetime] = Query(None, description="开始时间过滤"),
    to_time: Optional[datetime] = Query(None, description="结束时间过滤"),
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(50, ge=1, le=200, description="每页条数"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    # 构建查询
    query = db.query(OperationLog)
    
    # 应用过滤条件
    if user_id:
        query = query.filter(OperationLog.user_id == user_id)
    if action:
        query = query.filter(OperationLog.action == action)
    if entity_type:
        query = query.filter(OperationLog.entity_type == entity_type)
    if entity_id:
        query = query.filter(OperationLog.entity_id == entity_id)
    if success is not None:
        query = query.filter(OperationLog.success == success)
    if from_time:
        query = query.filter(OperationLog.created_at >= from_time)
    if to_time:
        query = query.filter(OperationLog.created_at <= to_time)
    
    # 计算总数
    total = query.count()
    
    # 应用分页
    skip = (page - 1) * page_size
    operation_logs = query.order_by(OperationLog.created_at.desc()).offset(skip).limit(page_size).all()
    
    # 转换为响应模型
    operation_log_list = [OperationLogResponse.from_orm(log) for log in operation_logs]
    
    return GeneralResponse(
        data=PaginatedOperationLogList(
            items=operation_log_list,
            page=page,
            page_size=page_size,
            total=total
        )
    )
