from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from uuid import uuid4
from typing import Optional, List
from app.core.auth import get_current_active_user
from app.core.config import settings
from app.core.database import get_db
from app.models.user import User
from app.models.ai_capability import AICapability
from app.models.task import FileType
from app.models.rule_item import OnFailStrategy
from app.schemas.ai_capability import (
    AICapabilityCreate, AICapabilityUpdate, 
    AICapabilityResponse, PaginatedAICapabilityList
)
from app.schemas.response import GeneralResponse

router = APIRouter(redirect_slashes=False)
admin_router = APIRouter(redirect_slashes=False)

# 管理员获取AI字段能力列表
@admin_router.get("/", response_model=GeneralResponse[List[AICapabilityResponse]], tags=["admin-ai-capabilities"])
async def admin_get_ai_capabilities(
    file_type: Optional[str] = Query(None, description="文件类型过滤"),
    enabled: Optional[bool] = Query(None, description="是否启用过滤"),
    target_column: Optional[str] = Query(None, description="目标列搜索"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    # 构建查询
    query = db.query(AICapability)
    
    # 应用过滤条件
    if file_type:
        query = query.filter(AICapability.file_type == FileType(file_type))
    if enabled is not None:
        query = query.filter(AICapability.enabled == enabled)
    if target_column:
        query = query.filter(AICapability.target_column == target_column)
    
    # 获取AI字段能力
    ai_capabilities = query.order_by(AICapability.created_at.desc()).all()
    
    # 转换为响应模型
    ai_capability_list = [AICapabilityResponse.from_orm(ai) for ai in ai_capabilities]
    
    return GeneralResponse(data=ai_capability_list)

# 管理员创建AI字段能力
@admin_router.post("/", response_model=GeneralResponse[dict], tags=["admin-ai-capabilities"])
async def admin_create_ai_capability(
    ai_capability_data: AICapabilityCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    # 创建AI字段能力
    ai_capability = AICapability(
        id=str(uuid4()),
        file_type=ai_capability_data.file_type,
        target_column=ai_capability_data.target_column,
        target_field_name=ai_capability_data.target_field_name,
        capability_code=ai_capability_data.capability_code,
        depends_on=ai_capability_data.depends_on,
        prompt_template=ai_capability_data.prompt_template,
        output_constraints_json=ai_capability_data.output_constraints_json,
        on_fail=ai_capability_data.on_fail,
        enabled=ai_capability_data.enabled,
        note=ai_capability_data.note
    )
    
    db.add(ai_capability)
    db.commit()
    db.refresh(ai_capability)
    
    return GeneralResponse(data={"id": ai_capability.id})

# 管理员更新AI字段能力
@admin_router.put("/{id}", response_model=GeneralResponse[dict], tags=["admin-ai-capabilities"])
async def admin_update_ai_capability(
    id: str,
    ai_capability_data: AICapabilityUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    # 获取AI字段能力
    ai_capability = db.query(AICapability).filter(AICapability.id == id).first()
    if not ai_capability:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"AI capability with id '{id}' not found"
        )
    
    # 更新字段
    update_data = ai_capability_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(ai_capability, field, value)
    
    db.commit()
    db.refresh(ai_capability)
    
    return GeneralResponse(data={"id": ai_capability.id})

# 获取AI字段能力列表
@router.get("/", response_model=GeneralResponse[PaginatedAICapabilityList], tags=["ai-capabilities"])
async def get_ai_capabilities(
    file_type: Optional[str] = Query(None, description="文件类型过滤"),
    target_column: Optional[str] = Query(None, description="目标列搜索"),
    enabled: Optional[bool] = Query(None, description="是否启用过滤"),
    capability_code: Optional[str] = Query(None, description="能力编码搜索"),
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页条数"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    # 构建查询
    query = db.query(AICapability)
    
    # 应用过滤条件
    if file_type:
        query = query.filter(AICapability.file_type == FileType(file_type))
    if target_column:
        query = query.filter(AICapability.target_column == target_column)
    if enabled is not None:
        query = query.filter(AICapability.enabled == enabled)
    if capability_code:
        query = query.filter(AICapability.capability_code.contains(capability_code))
    
    # 计算总数
    total = query.count()
    
    # 应用分页
    skip = (page - 1) * page_size
    ai_capabilities = query.order_by(AICapability.created_at.desc()).offset(skip).limit(page_size).all()
    
    # 转换为响应模型
    ai_capability_list = [AICapabilityResponse.from_orm(ai) for ai in ai_capabilities]
    
    return GeneralResponse(
        data=PaginatedAICapabilityList(
            items=ai_capability_list,
            page=page,
            page_size=page_size,
            total=total
        )
    )

# 创建AI字段能力
@router.post("/", response_model=GeneralResponse[AICapabilityResponse], tags=["ai-capabilities"])
async def create_ai_capability(
    ai_capability_data: AICapabilityCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    # 创建AI字段能力
    ai_capability = AICapability(
        id=str(uuid4()),
        file_type=ai_capability_data.file_type,
        target_column=ai_capability_data.target_column,
        target_field_name=ai_capability_data.target_field_name,
        capability_code=ai_capability_data.capability_code,
        depends_on=ai_capability_data.depends_on,
        prompt_template=ai_capability_data.prompt_template,
        output_constraints_json=ai_capability_data.output_constraints_json,
        on_fail=ai_capability_data.on_fail,
        enabled=ai_capability_data.enabled,
        note=ai_capability_data.note
    )
    
    db.add(ai_capability)
    db.commit()
    db.refresh(ai_capability)
    
    return GeneralResponse(data=AICapabilityResponse.from_orm(ai_capability))

# 获取AI字段能力详情
@router.get("/{id}", response_model=GeneralResponse[AICapabilityResponse], tags=["ai-capabilities"])
async def get_ai_capability(
    id: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    ai_capability = db.query(AICapability).filter(AICapability.id == id).first()
    if not ai_capability:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"AI capability with id '{id}' not found"
        )
    
    return GeneralResponse(data=AICapabilityResponse.from_orm(ai_capability))

# 更新AI字段能力
@router.put("/{id}", response_model=GeneralResponse[AICapabilityResponse], tags=["ai-capabilities"])
async def update_ai_capability(
    id: str,
    ai_capability_data: AICapabilityUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    ai_capability = db.query(AICapability).filter(AICapability.id == id).first()
    if not ai_capability:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"AI capability with id '{id}' not found"
        )
    
    # 更新字段
    update_data = ai_capability_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(ai_capability, field, value)
    
    db.commit()
    db.refresh(ai_capability)
    
    return GeneralResponse(data=AICapabilityResponse.from_orm(ai_capability))

# 删除AI字段能力
@router.delete("/{id}", response_model=GeneralResponse[dict], tags=["ai-capabilities"])
async def delete_ai_capability(
    id: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    ai_capability = db.query(AICapability).filter(AICapability.id == id).first()
    if not ai_capability:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"AI capability with id '{id}' not found"
        )
    
    db.delete(ai_capability)
    db.commit()
    
    return GeneralResponse(data={"message": f"AI capability '{ai_capability.capability_code}' deleted successfully"})

# 启用AI字段能力
@router.put("/{id}/enable", response_model=GeneralResponse[AICapabilityResponse], tags=["ai-capabilities"])
async def enable_ai_capability(
    id: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    ai_capability = db.query(AICapability).filter(AICapability.id == id).first()
    if not ai_capability:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"AI capability with id '{id}' not found"
        )
    
    ai_capability.enabled = True
    db.commit()
    db.refresh(ai_capability)
    
    return GeneralResponse(data=AICapabilityResponse.from_orm(ai_capability))

# 禁用AI字段能力
@router.put("/{id}/disable", response_model=GeneralResponse[AICapabilityResponse], tags=["ai-capabilities"])
async def disable_ai_capability(
    id: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    ai_capability = db.query(AICapability).filter(AICapability.id == id).first()
    if not ai_capability:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"AI capability with id '{id}' not found"
        )
    
    ai_capability.enabled = False
    db.commit()
    db.refresh(ai_capability)
    
    return GeneralResponse(data=AICapabilityResponse.from_orm(ai_capability))
