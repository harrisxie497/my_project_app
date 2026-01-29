from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional
from app.core.auth import get_current_active_user
from app.core.database import get_db
from app.models.user import User
from app.models.rule_definition import RuleDefinition
from app.schemas.rule_definition import (
    RuleDefinitionCreate, RuleDefinitionUpdate, 
    RuleDefinitionResponse, PaginatedRuleDefinitionList
)
from app.schemas.response import GeneralResponse

# 创建路由器，与任务中心保持一致
router = APIRouter(redirect_slashes=False)

# 获取规则定义列表
@router.get("", response_model=GeneralResponse[PaginatedRuleDefinitionList], tags=["rule-definitions"])
async def get_rule_definitions(
    rule_type: Optional[str] = Query(None, description="规则类型过滤"),
    executor_type: Optional[str] = Query(None, description="执行器类型过滤"),
    enabled: Optional[bool] = Query(None, description="启用状态过滤"),
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页条数"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    # 构建查询
    query = db.query(RuleDefinition)
    
    # 应用过滤条件
    if rule_type:
        query = query.filter(RuleDefinition.rule_type == rule_type)
    if executor_type:
        query = query.filter(RuleDefinition.executor_type == executor_type)
    if enabled is not None:
        query = query.filter(RuleDefinition.enabled == enabled)
    
    # 计算总数
    total = query.count()
    
    # 应用分页
    skip = (page - 1) * page_size
    rule_definitions = query.order_by(RuleDefinition.rule_ref).offset(skip).limit(page_size).all()
    
    # 转换为响应模型
    rule_definition_list = [RuleDefinitionResponse.from_orm(rd) for rd in rule_definitions]
    
    return GeneralResponse(
        data=PaginatedRuleDefinitionList(
            items=rule_definition_list,
            page=page,
            page_size=page_size,
            total=total
        )
    )

# 获取单个规则定义
@router.get("/{rule_ref}", response_model=GeneralResponse[RuleDefinitionResponse], tags=["rule-definitions"])
async def get_rule_definition(
    rule_ref: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    rule_definition = db.query(RuleDefinition).filter(RuleDefinition.rule_ref == rule_ref).first()
    if not rule_definition:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Rule definition with rule_ref '{rule_ref}' not found"
        )
    
    return GeneralResponse(data=RuleDefinitionResponse.from_orm(rule_definition))

# 创建规则定义
@router.post("", response_model=GeneralResponse[RuleDefinitionResponse], tags=["rule-definitions"])
async def create_rule_definition(
    rule_definition_data: RuleDefinitionCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    # 检查规则引用是否已存在
    existing = db.query(RuleDefinition).filter(RuleDefinition.rule_ref == rule_definition_data.rule_ref).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Rule definition with rule_ref '{rule_definition_data.rule_ref}' already exists"
        )
    
    # 创建规则定义
    rule_definition = RuleDefinition(
        **rule_definition_data.model_dump()
    )
    
    db.add(rule_definition)
    db.commit()
    db.refresh(rule_definition)
    
    return GeneralResponse(data=RuleDefinitionResponse.from_orm(rule_definition))

# 更新规则定义
@router.put("/{rule_ref}", response_model=GeneralResponse[RuleDefinitionResponse], tags=["rule-definitions"])
async def update_rule_definition(
    rule_ref: str,
    rule_definition_data: RuleDefinitionUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    rule_definition = db.query(RuleDefinition).filter(RuleDefinition.rule_ref == rule_ref).first()
    if not rule_definition:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Rule definition with rule_ref '{rule_ref}' not found"
        )
    
    # 更新字段
    update_data = rule_definition_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(rule_definition, field, value)
    
    db.commit()
    db.refresh(rule_definition)
    
    return GeneralResponse(data=RuleDefinitionResponse.from_orm(rule_definition))

# 删除规则定义
@router.delete("/{rule_ref}", response_model=GeneralResponse[dict], tags=["rule-definitions"])
async def delete_rule_definition(
    rule_ref: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    rule_definition = db.query(RuleDefinition).filter(RuleDefinition.rule_ref == rule_ref).first()
    if not rule_definition:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Rule definition with rule_ref '{rule_ref}' not found"
        )
    
    db.delete(rule_definition)
    db.commit()
    
    return GeneralResponse(data={"message": f"Rule definition '{rule_ref}' deleted successfully"})

# 启用/禁用规则定义
@router.patch("/{rule_ref}/status", response_model=GeneralResponse[RuleDefinitionResponse], tags=["rule-definitions"])
async def update_rule_definition_status(
    rule_ref: str,
    enabled: bool = Query(..., description="启用状态"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    rule_definition = db.query(RuleDefinition).filter(RuleDefinition.rule_ref == rule_ref).first()
    if not rule_definition:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Rule definition with rule_ref '{rule_ref}' not found"
        )
    
    # 更新启用状态
    rule_definition.enabled = enabled
    db.commit()
    db.refresh(rule_definition)
    
    return GeneralResponse(data=RuleDefinitionResponse.from_orm(rule_definition))