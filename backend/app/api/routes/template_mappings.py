from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from uuid import uuid4
from typing import Optional, List
from app.core.auth import get_current_active_user
from app.core.config import settings
from app.core.database import get_db
from app.models.user import User
from app.models.template_mapping import TemplateMapping, SheetMatchMode
from app.models.task import FileType
from app.schemas.template_mapping import (
    TemplateMappingCreate, TemplateMappingUpdate, 
    TemplateMappingResponse, PaginatedTemplateMappingList
)
from app.schemas.response import GeneralResponse

router = APIRouter(redirect_slashes=False)
admin_router = APIRouter(redirect_slashes=False)

# 管理员获取模板映射列表
@admin_router.get("/", response_model=GeneralResponse[List[TemplateMappingResponse]], tags=["admin-template-mappings"])
async def admin_get_template_mappings(
    file_type: Optional[str] = Query(None, description="文件类型过滤"),
    enabled: Optional[bool] = Query(None, description="是否启用过滤"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    # 构建查询
    query = db.query(TemplateMapping)
    
    # 应用过滤条件
    if file_type:
        query = query.filter(TemplateMapping.file_type == FileType(file_type))
    if enabled is not None:
        query = query.filter(TemplateMapping.enabled == enabled)
    
    # 获取模板映射
    template_mappings = query.order_by(TemplateMapping.created_at.desc()).all()
    
    # 转换为响应模型
    mapping_list = [TemplateMappingResponse.from_orm(tm) for tm in template_mappings]
    
    return GeneralResponse(data=mapping_list)

# 管理员创建模板映射
@admin_router.post("/", response_model=GeneralResponse[dict], tags=["admin-template-mappings"])
async def admin_create_template_mapping(
    mapping_data: TemplateMappingCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    # 检查映射编码是否已存在
    existing_mapping = db.query(TemplateMapping).filter(
        TemplateMapping.mapping_code == mapping_data.mapping_code
    ).first()
    if existing_mapping:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Template mapping with code '{mapping_data.mapping_code}' already exists"
        )
    
    # 创建模板映射
    template_mapping = TemplateMapping(
        id=str(uuid4()),
        mapping_code=mapping_data.mapping_code,
        file_type=mapping_data.file_type,
        source_template_code=mapping_data.source_template_code,
        target_template_code=mapping_data.target_template_code,
        sheet_match_mode=mapping_data.sheet_match_mode,
        sheet_match_value=mapping_data.sheet_match_value,
        column_bindings_json=mapping_data.column_bindings_json,
        enabled=mapping_data.enabled,
        note=mapping_data.note
    )
    
    db.add(template_mapping)
    db.commit()
    db.refresh(template_mapping)
    
    return GeneralResponse(data={"id": template_mapping.id})

# 管理员更新模板映射
@admin_router.put("/{id}", response_model=GeneralResponse[dict], tags=["admin-template-mappings"])
async def admin_update_template_mapping(
    id: str,
    mapping_data: TemplateMappingUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    # 获取模板映射
    template_mapping = db.query(TemplateMapping).filter(TemplateMapping.id == id).first()
    if not template_mapping:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Template mapping with id '{id}' not found"
        )
    
    # 更新字段
    update_data = mapping_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(template_mapping, field, value)
    
    db.commit()
    db.refresh(template_mapping)
    
    return GeneralResponse(data={"id": template_mapping.id})

# 管理员模板映射自检
@admin_router.post("/{id}/validate", response_model=GeneralResponse[dict], tags=["admin-template-mappings"])
async def admin_validate_template_mapping(
    id: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    # 获取模板映射
    template_mapping = db.query(TemplateMapping).filter(TemplateMapping.id == id).first()
    if not template_mapping:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Template mapping with id '{id}' not found"
        )
    
    # 这里可以添加模板映射自检的具体实现逻辑
    # 例如：验证json格式、检查必填字段、验证绑定关系等
    
    # 目前返回模拟数据
    validation_result = {
        "valid": True,
        "warnings": []
    }
    
    return GeneralResponse(data=validation_result)

# 获取模板映射列表
@router.get("/", response_model=GeneralResponse[PaginatedTemplateMappingList], tags=["template-mappings"])
async def get_template_mappings(
    file_type: Optional[str] = Query(None, description="文件类型过滤"),
    enabled: Optional[bool] = Query(None, description="是否启用过滤"),
    mapping_code: Optional[str] = Query(None, description="映射编码搜索"),
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页条数"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    # 构建查询
    query = db.query(TemplateMapping)
    
    # 应用过滤条件
    if file_type:
        query = query.filter(TemplateMapping.file_type == FileType(file_type))
    if enabled is not None:
        query = query.filter(TemplateMapping.enabled == enabled)
    if mapping_code:
        query = query.filter(TemplateMapping.mapping_code.contains(mapping_code))
    
    # 计算总数
    total = query.count()
    
    # 应用分页
    skip = (page - 1) * page_size
    template_mappings = query.order_by(TemplateMapping.created_at.desc()).offset(skip).limit(page_size).all()
    
    # 转换为响应模型
    mapping_list = [TemplateMappingResponse.from_orm(tm) for tm in template_mappings]
    
    return GeneralResponse(
        data=PaginatedTemplateMappingList(
            items=mapping_list,
            page=page,
            page_size=page_size,
            total=total
        )
    )

# 创建模板映射
@router.post("/", response_model=GeneralResponse[TemplateMappingResponse], tags=["template-mappings"])
async def create_template_mapping(
    mapping_data: TemplateMappingCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    # 检查映射编码是否已存在
    existing_mapping = db.query(TemplateMapping).filter(
        TemplateMapping.mapping_code == mapping_data.mapping_code
    ).first()
    if existing_mapping:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Template mapping with code '{mapping_data.mapping_code}' already exists"
        )
    
    # 创建模板映射
    template_mapping = TemplateMapping(
        id=str(uuid4()),
        mapping_code=mapping_data.mapping_code,
        file_type=mapping_data.file_type,
        source_template_code=mapping_data.source_template_code,
        target_template_code=mapping_data.target_template_code,
        sheet_match_mode=mapping_data.sheet_match_mode,
        sheet_match_value=mapping_data.sheet_match_value,
        column_bindings_json=mapping_data.column_bindings_json,
        enabled=mapping_data.enabled,
        note=mapping_data.note
    )
    
    db.add(template_mapping)
    db.commit()
    db.refresh(template_mapping)
    
    return GeneralResponse(data=TemplateMappingResponse.from_orm(template_mapping))

# 获取模板映射详情
@router.get("/{id}", response_model=GeneralResponse[TemplateMappingResponse], tags=["template-mappings"])
async def get_template_mapping(
    id: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    template_mapping = db.query(TemplateMapping).filter(TemplateMapping.id == id).first()
    if not template_mapping:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Template mapping with id '{id}' not found"
        )
    
    return GeneralResponse(data=TemplateMappingResponse.from_orm(template_mapping))

# 更新模板映射
@router.put("/{id}", response_model=GeneralResponse[TemplateMappingResponse], tags=["template-mappings"])
async def update_template_mapping(
    id: str,
    mapping_data: TemplateMappingUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    template_mapping = db.query(TemplateMapping).filter(TemplateMapping.id == id).first()
    if not template_mapping:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Template mapping with id '{id}' not found"
        )
    
    # 更新字段
    update_data = mapping_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(template_mapping, field, value)
    
    db.commit()
    db.refresh(template_mapping)
    
    return GeneralResponse(data=TemplateMappingResponse.from_orm(template_mapping))

# 删除模板映射
@router.delete("/{id}", response_model=GeneralResponse[dict], tags=["template-mappings"])
async def delete_template_mapping(
    id: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    template_mapping = db.query(TemplateMapping).filter(TemplateMapping.id == id).first()
    if not template_mapping:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Template mapping with id '{id}' not found"
        )
    
    db.delete(template_mapping)
    db.commit()
    
    return GeneralResponse(data={"message": f"Template mapping '{template_mapping.mapping_code}' deleted successfully"})

# 启用模板映射
@router.put("/{id}/enable", response_model=GeneralResponse[TemplateMappingResponse], tags=["template-mappings"])
async def enable_template_mapping(
    id: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    template_mapping = db.query(TemplateMapping).filter(TemplateMapping.id == id).first()
    if not template_mapping:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Template mapping with id '{id}' not found"
        )
    
    template_mapping.enabled = True
    db.commit()
    db.refresh(template_mapping)
    
    return GeneralResponse(data=TemplateMappingResponse.from_orm(template_mapping))

# 禁用模板映射
@router.put("/{id}/disable", response_model=GeneralResponse[TemplateMappingResponse], tags=["template-mappings"])
async def disable_template_mapping(
    id: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    template_mapping = db.query(TemplateMapping).filter(TemplateMapping.id == id).first()
    if not template_mapping:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Template mapping with id '{id}' not found"
        )
    
    template_mapping.enabled = False
    db.commit()
    db.refresh(template_mapping)
    
    return GeneralResponse(data=TemplateMappingResponse.from_orm(template_mapping))

# 模板映射自检
@router.post("/{id}/validate", response_model=GeneralResponse[dict], tags=["template-mappings"])
async def validate_template_mapping(
    id: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    # 获取模板映射
    template_mapping = db.query(TemplateMapping).filter(TemplateMapping.id == id).first()
    if not template_mapping:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Template mapping with id '{id}' not found"
        )
    
    # 这里可以添加模板映射自检的具体实现逻辑
    # 例如：验证json格式、检查必填字段、验证绑定关系等
    
    # 目前返回模拟数据
    validation_result = {
        "valid": True,
        "warnings": []
    }
    
    return GeneralResponse(data=validation_result)
