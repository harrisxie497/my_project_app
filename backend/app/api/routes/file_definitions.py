from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from uuid import uuid4
from typing import Optional
from app.core.auth import get_current_active_user
from app.core.database import get_db
from app.models.user import User
from app.models.file_definition import FileDefinition
from app.schemas.file_definition import (
    FileDefinitionCreate, FileDefinitionUpdate, 
    FileDefinitionResponse, PaginatedFileDefinitionList
)
from app.schemas.response import GeneralResponse

# 创建路由器，与任务中心保持一致
router = APIRouter(redirect_slashes=False)

# 获取文件定义列表
@router.get("", response_model=GeneralResponse[PaginatedFileDefinitionList], tags=["file-definitions"])
async def get_file_definitions(
    file_type: Optional[str] = Query(None, description="文件类型过滤"),
    file_role: Optional[str] = Query(None, description="文件角色过滤"),
    enabled: Optional[bool] = Query(None, description="启用状态过滤"),
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页条数"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    # 构建查询
    query = db.query(FileDefinition)
    
    # 应用过滤条件
    if file_type:
        query = query.filter(FileDefinition.file_type == file_type)
    if file_role:
        query = query.filter(FileDefinition.file_role == file_role)
    if enabled is not None:
        query = query.filter(FileDefinition.enabled == enabled)
    
    # 计算总数
    total = query.count()
    
    # 应用分页
    skip = (page - 1) * page_size
    file_definitions = query.order_by(FileDefinition.created_at.desc()).offset(skip).limit(page_size).all()
    
    # 转换为响应模型
    file_definition_list = [FileDefinitionResponse.from_orm(fd) for fd in file_definitions]
    
    return GeneralResponse(
        data=PaginatedFileDefinitionList(
            items=file_definition_list,
            page=page,
            page_size=page_size,
            total=total
        )
    )

# 获取单个文件定义
@router.get("/{id}", response_model=GeneralResponse[FileDefinitionResponse], tags=["file-definitions"])
async def get_file_definition(
    id: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    file_definition = db.query(FileDefinition).filter(FileDefinition.id == id).first()
    if not file_definition:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"File definition with id '{id}' not found"
        )
    
    return GeneralResponse(data=FileDefinitionResponse.from_orm(file_definition))

# 创建文件定义
@router.post("", response_model=GeneralResponse[FileDefinitionResponse], tags=["file-definitions"])
async def create_file_definition(
    file_definition_data: FileDefinitionCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    # 创建文件定义
    file_definition = FileDefinition(
        id=str(uuid4()),
        **file_definition_data.model_dump()
    )
    
    db.add(file_definition)
    db.commit()
    db.refresh(file_definition)
    
    return GeneralResponse(data=FileDefinitionResponse.from_orm(file_definition))

# 更新文件定义
@router.put("/{id}", response_model=GeneralResponse[FileDefinitionResponse], tags=["file-definitions"])
async def update_file_definition(
    id: str,
    file_definition_data: FileDefinitionUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    file_definition = db.query(FileDefinition).filter(FileDefinition.id == id).first()
    if not file_definition:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"File definition with id '{id}' not found"
        )
    
    # 更新字段
    update_data = file_definition_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(file_definition, field, value)
    
    db.commit()
    db.refresh(file_definition)
    
    return GeneralResponse(data=FileDefinitionResponse.from_orm(file_definition))

# 删除文件定义
@router.delete("/{id}", response_model=GeneralResponse[dict], tags=["file-definitions"])
async def delete_file_definition(
    id: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    file_definition = db.query(FileDefinition).filter(FileDefinition.id == id).first()
    if not file_definition:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"File definition with id '{id}' not found"
        )
    
    db.delete(file_definition)
    db.commit()
    
    return GeneralResponse(data={"message": f"File definition '{file_definition.file_type} - {file_definition.file_role}' deleted successfully"})

# 启用/禁用文件定义
@router.patch("/{id}/status", response_model=GeneralResponse[FileDefinitionResponse], tags=["file-definitions"])
async def update_file_definition_status(
    id: str,
    enabled: bool = Query(..., description="启用状态"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    file_definition = db.query(FileDefinition).filter(FileDefinition.id == id).first()
    if not file_definition:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"File definition with id '{id}' not found"
        )
    
    # 更新启用状态
    file_definition.enabled = enabled
    db.commit()
    db.refresh(file_definition)
    
    return GeneralResponse(data=FileDefinitionResponse.from_orm(file_definition))
