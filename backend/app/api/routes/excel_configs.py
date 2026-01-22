from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from uuid import uuid4
from typing import Optional, List
from app.core.auth import get_current_active_user
from app.core.config import settings
from app.core.database import get_db
from app.models.user import User
from app.models.excel_config import ExcelConfig
from app.models.task import FileType
from app.schemas.excel_config import (
    ExcelConfigCreate, ExcelConfigUpdate, 
    ExcelConfigResponse, PaginatedExcelConfigList
)
from app.schemas.response import GeneralResponse

router = APIRouter(redirect_slashes=False)
admin_router = APIRouter(redirect_slashes=False)

# 获取Excel配置列表
@router.get("/", response_model=GeneralResponse[PaginatedExcelConfigList], tags=["excel-configs"])
async def get_excel_configs(
    file_type: Optional[str] = Query(None, description="文件类型过滤"),
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页条数"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    # 构建查询
    query = db.query(ExcelConfig)
    
    # 应用过滤条件
    if file_type:
        query = query.filter(ExcelConfig.file_type == FileType(file_type))
    
    # 计算总数
    total = query.count()
    
    # 应用分页
    skip = (page - 1) * page_size
    excel_configs = query.order_by(ExcelConfig.created_at.desc()).offset(skip).limit(page_size).all()
    
    # 转换为响应模型
    excel_config_list = [ExcelConfigResponse.from_orm(ec) for ec in excel_configs]
    
    return GeneralResponse(
        data=PaginatedExcelConfigList(
            items=excel_config_list,
            page=page,
            page_size=page_size,
            total=total
        )
    )

# 获取Excel配置详情
@router.get("/{id}", response_model=GeneralResponse[ExcelConfigResponse], tags=["excel-configs"])
async def get_excel_config(
    id: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    excel_config = db.query(ExcelConfig).filter(ExcelConfig.id == id).first()
    if not excel_config:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Excel config with id '{id}' not found"
        )
    
    return GeneralResponse(data=ExcelConfigResponse.from_orm(excel_config))

# 创建Excel配置
@router.post("/", response_model=GeneralResponse[ExcelConfigResponse], tags=["excel-configs"])
async def create_excel_config(
    excel_config_data: ExcelConfigCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    # 检查是否已存在相同文件类型的配置
    existing_config = db.query(ExcelConfig).filter(
        ExcelConfig.file_type == excel_config_data.file_type
    ).first()
    if existing_config:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Excel config for file type '{excel_config_data.file_type}' already exists"
        )
    
    # 创建Excel配置
    excel_config = ExcelConfig(
        id=str(uuid4()),
        file_type=excel_config_data.file_type,
        default_font=excel_config_data.default_font,
        date_format=excel_config_data.date_format,
        merge_ranges=excel_config_data.merge_ranges,
        style_rules=excel_config_data.style_rules
    )
    
    db.add(excel_config)
    db.commit()
    db.refresh(excel_config)
    
    return GeneralResponse(data=ExcelConfigResponse.from_orm(excel_config))

# 更新Excel配置
@router.put("/{id}", response_model=GeneralResponse[ExcelConfigResponse], tags=["excel-configs"])
async def update_excel_config(
    id: str,
    excel_config_data: ExcelConfigUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    excel_config = db.query(ExcelConfig).filter(ExcelConfig.id == id).first()
    if not excel_config:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Excel config with id '{id}' not found"
        )
    
    # 更新字段
    update_data = excel_config_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(excel_config, field, value)
    
    db.commit()
    db.refresh(excel_config)
    
    return GeneralResponse(data=ExcelConfigResponse.from_orm(excel_config))

# 删除Excel配置
@router.delete("/{id}", response_model=GeneralResponse[dict], tags=["excel-configs"])
async def delete_excel_config(
    id: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    excel_config = db.query(ExcelConfig).filter(ExcelConfig.id == id).first()
    if not excel_config:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Excel config with id '{id}' not found"
        )
    
    db.delete(excel_config)
    db.commit()
    
    return GeneralResponse(data={"message": f"Excel config for '{excel_config.file_type}' deleted successfully"})

# 管理员获取当前Excel配置
@admin_router.get("/active", response_model=GeneralResponse[ExcelConfigResponse], tags=["admin-excel-configs"])
async def admin_get_active_excel_config(
    file_type: str = Query(..., description="文件类型"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    # 查找指定文件类型的最新配置
    excel_config = db.query(ExcelConfig).filter(
        ExcelConfig.file_type == FileType(file_type)
    ).order_by(ExcelConfig.created_at.desc()).first()
    
    if not excel_config:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Excel config for file type '{file_type}' not found"
        )
    
    return GeneralResponse(data=ExcelConfigResponse.from_orm(excel_config))

# 管理员更新当前Excel配置
@admin_router.put("/active", response_model=GeneralResponse[ExcelConfigResponse], tags=["admin-excel-configs"])
async def admin_update_active_excel_config(
    excel_config_data: ExcelConfigCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    # 查找指定文件类型的最新配置
    existing_config = db.query(ExcelConfig).filter(
        ExcelConfig.file_type == excel_config_data.file_type
    ).order_by(ExcelConfig.created_at.desc()).first()
    
    if existing_config:
        # 更新现有配置
        update_data = excel_config_data.model_dump()
        for field, value in update_data.items():
            setattr(existing_config, field, value)
        
        db.commit()
        db.refresh(existing_config)
        return GeneralResponse(data=ExcelConfigResponse.from_orm(existing_config))
    else:
        # 创建新配置
        excel_config = ExcelConfig(
            id=str(uuid4()),
            **excel_config_data.model_dump()
        )
        
        db.add(excel_config)
        db.commit()
        db.refresh(excel_config)
        return GeneralResponse(data=ExcelConfigResponse.from_orm(excel_config))
