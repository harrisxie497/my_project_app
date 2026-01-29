from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from uuid import uuid4
from typing import Optional
from app.core.auth import get_current_active_user
from app.core.database import get_db
from app.models.user import User
from app.models.field_pipeline import FieldPipeline
from app.schemas.field_pipeline import (
    FieldPipelineCreate, FieldPipelineUpdate, 
    FieldPipelineResponse, PaginatedFieldPipelineList
)
from app.schemas.response import GeneralResponse

# 创建路由器，与任务中心保持一致
router = APIRouter(redirect_slashes=False)

# 获取字段映射列表
@router.get("", response_model=GeneralResponse[PaginatedFieldPipelineList], tags=["field-pipelines"])
async def get_field_pipelines(
    file_type: Optional[str] = Query(None, description="文件类型过滤"),
    target_col: Optional[str] = Query(None, description="目标列过滤"),
    field_type: Optional[str] = Query(None, description="字段类型过滤"),
    enabled: Optional[bool] = Query(None, description="启用状态过滤"),
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页条数"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    # 构建查询
    query = db.query(FieldPipeline)
    
    # 应用过滤条件
    if file_type:
        query = query.filter(FieldPipeline.file_type == file_type)
    if target_col:
        query = query.filter(FieldPipeline.target_col == target_col)
    if field_type:
        query = query.filter(FieldPipeline.field_type == field_type)
    if enabled is not None:
        query = query.filter(FieldPipeline.enabled == enabled)
    
    # 计算总数
    total = query.count()
    
    # 应用分页
    skip = (page - 1) * page_size
    field_pipelines = query.order_by(FieldPipeline.order).offset(skip).limit(page_size).all()
    
    # 转换为响应模型
    field_pipeline_list = [FieldPipelineResponse.from_orm(fp) for fp in field_pipelines]
    
    return GeneralResponse(
        data=PaginatedFieldPipelineList(
            items=field_pipeline_list,
            page=page,
            page_size=page_size,
            total=total
        )
    )

# 获取单个字段映射
@router.get("/{id}", response_model=GeneralResponse[FieldPipelineResponse], tags=["field-pipelines"])
async def get_field_pipeline(
    id: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    field_pipeline = db.query(FieldPipeline).filter(FieldPipeline.id == id).first()
    if not field_pipeline:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Field pipeline with id '{id}' not found"
        )
    
    return GeneralResponse(data=FieldPipelineResponse.from_orm(field_pipeline))

# 创建字段映射
@router.post("", response_model=GeneralResponse[FieldPipelineResponse], tags=["field-pipelines"])
async def create_field_pipeline(
    field_pipeline_data: FieldPipelineCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    # 创建字段映射
    field_pipeline = FieldPipeline(
        id=str(uuid4()),
        **field_pipeline_data.model_dump()
    )
    
    db.add(field_pipeline)
    db.commit()
    db.refresh(field_pipeline)
    
    return GeneralResponse(data=FieldPipelineResponse.from_orm(field_pipeline))

# 更新字段映射
@router.put("/{id}", response_model=GeneralResponse[FieldPipelineResponse], tags=["field-pipelines"])
async def update_field_pipeline(
    id: str,
    field_pipeline_data: FieldPipelineUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    field_pipeline = db.query(FieldPipeline).filter(FieldPipeline.id == id).first()
    if not field_pipeline:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Field pipeline with id '{id}' not found"
        )
    
    # 更新字段
    update_data = field_pipeline_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(field_pipeline, field, value)
    
    db.commit()
    db.refresh(field_pipeline)
    
    return GeneralResponse(data=FieldPipelineResponse.from_orm(field_pipeline))

# 删除字段映射
@router.delete("/{id}", response_model=GeneralResponse[dict], tags=["field-pipelines"])
async def delete_field_pipeline(
    id: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    field_pipeline = db.query(FieldPipeline).filter(FieldPipeline.id == id).first()
    if not field_pipeline:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Field pipeline with id '{id}' not found"
        )
    
    db.delete(field_pipeline)
    db.commit()
    
    return GeneralResponse(data={"message": f"Field pipeline for '{field_pipeline.target_col}' deleted successfully"})

# 启用/禁用字段映射
@router.patch("/{id}/status", response_model=GeneralResponse[FieldPipelineResponse], tags=["field-pipelines"])
async def update_field_pipeline_status(
    id: str,
    enabled: bool = Query(..., description="启用状态"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    field_pipeline = db.query(FieldPipeline).filter(FieldPipeline.id == id).first()
    if not field_pipeline:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Field pipeline with id '{id}' not found"
        )
    
    # 更新启用状态
    field_pipeline.enabled = enabled
    db.commit()
    db.refresh(field_pipeline)
    
    return GeneralResponse(data=FieldPipelineResponse.from_orm(field_pipeline))

# 获取执行顺序
@router.get("/execution-order/{file_type}", response_model=GeneralResponse[list[FieldPipelineResponse]], tags=["field-pipelines"])
async def get_execution_order(
    file_type: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    # 查询指定文件类型的字段映射，按执行顺序排列
    field_pipelines = db.query(FieldPipeline).filter(
        FieldPipeline.file_type == file_type,
        FieldPipeline.enabled == True
    ).order_by(FieldPipeline.order).all()
    
    if not field_pipelines:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No field pipelines found for file type '{file_type}'"
        )
    
    # 转换为响应模型
    field_pipeline_list = [FieldPipelineResponse.from_orm(fp) for fp in field_pipelines]
    
    return GeneralResponse(data=field_pipeline_list)
