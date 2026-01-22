from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from uuid import uuid4
from typing import Optional, List
from app.core.auth import get_current_active_user
from app.core.config import settings
from app.core.database import get_db
from app.models.user import User
from app.models.rule_table import RuleTable, RuleStage
from app.models.task import FileType
from app.schemas.rule_table import (
    RuleTableCreate, RuleTableUpdate, RuleTableResponse, PaginatedRuleTableList
)
from app.schemas.response import GeneralResponse

router = APIRouter(redirect_slashes=False)
admin_router = APIRouter(redirect_slashes=False)

# 管理员获取规则表列表
@admin_router.get("/", response_model=GeneralResponse[List[RuleTableResponse]], tags=["admin-rule-tables"])
async def admin_get_rule_tables(
    file_type: Optional[str] = Query(None, description="文件类型过滤"),
    rule_stage: Optional[str] = Query(None, description="规则阶段过滤"),
    enabled: Optional[bool] = Query(None, description="是否启用过滤"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    # 构建查询
    query = db.query(RuleTable)
    
    # 应用过滤条件
    if file_type:
        query = query.filter(RuleTable.file_type == FileType(file_type))
    if rule_stage:
        query = query.filter(RuleTable.rule_stage == RuleStage(rule_stage))
    if enabled is not None:
        query = query.filter(RuleTable.enabled == enabled)
    
    # 获取规则表
    rule_tables = query.order_by(RuleTable.created_at.desc()).all()
    
    # 转换为响应模型
    rule_table_list = [RuleTableResponse.from_orm(rt) for rt in rule_tables]
    
    return GeneralResponse(data=rule_table_list)

# 管理员创建规则表
@admin_router.post("/", response_model=GeneralResponse[dict], tags=["admin-rule-tables"])
async def admin_create_rule_table(
    rule_table_data: RuleTableCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    # 检查规则表编码是否已存在
    existing_rule_table = db.query(RuleTable).filter(RuleTable.code == rule_table_data.code).first()
    if existing_rule_table:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Rule table with code '{rule_table_data.code}' already exists"
        )
    
    # 创建规则表
    rule_table = RuleTable(
        id=str(uuid4()),
        code=rule_table_data.code,
        name=rule_table_data.name,
        file_type=rule_table_data.file_type,
        rule_stage=rule_table_data.rule_stage,
        enabled=rule_table_data.enabled,
        description=rule_table_data.description
    )
    
    db.add(rule_table)
    db.commit()
    db.refresh(rule_table)
    
    return GeneralResponse(data={"id": rule_table.id})

# 管理员更新规则表
@admin_router.put("/{rule_table_id}", response_model=GeneralResponse[dict], tags=["admin-rule-tables"])
async def admin_update_rule_table(
    rule_table_id: str,
    rule_table_data: RuleTableUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    # 检查规则表是否存在
    rule_table = db.query(RuleTable).filter(RuleTable.id == rule_table_id).first()
    if not rule_table:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Rule table with id '{rule_table_id}' not found"
        )
    
    # 更新字段
    update_data = rule_table_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(rule_table, field, value)
    
    db.commit()
    db.refresh(rule_table)
    
    return GeneralResponse(data={"id": rule_table.id})

# 获取规则表列表
@router.get("/", response_model=GeneralResponse[PaginatedRuleTableList], tags=["rule-tables"])
async def get_rule_tables(
    file_type: Optional[str] = Query(None, description="文件类型过滤"),
    rule_stage: Optional[str] = Query(None, description="规则阶段过滤"),
    enabled: Optional[bool] = Query(None, description="是否启用过滤"),
    code: Optional[str] = Query(None, description="规则表编码搜索"),
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页条数"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    # 构建查询
    query = db.query(RuleTable)
    
    # 应用过滤条件
    if file_type:
        query = query.filter(RuleTable.file_type == FileType(file_type))
    if rule_stage:
        query = query.filter(RuleTable.rule_stage == RuleStage(rule_stage))
    if enabled is not None:
        query = query.filter(RuleTable.enabled == enabled)
    if code:
        query = query.filter(RuleTable.code.contains(code))
    
    # 计算总数
    total = query.count()
    
    # 应用分页
    skip = (page - 1) * page_size
    rule_tables = query.order_by(RuleTable.created_at.desc()).offset(skip).limit(page_size).all()
    
    # 转换为响应模型
    rule_table_list = [RuleTableResponse.from_orm(rt) for rt in rule_tables]
    
    return GeneralResponse(
        data=PaginatedRuleTableList(
            items=rule_table_list,
            page=page,
            page_size=page_size,
            total=total
        )
    )

# 创建规则表
@router.post("/", response_model=GeneralResponse[RuleTableResponse], tags=["rule-tables"])
async def create_rule_table(
    rule_table_data: RuleTableCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    # 检查规则表编码是否已存在
    existing_rule_table = db.query(RuleTable).filter(RuleTable.code == rule_table_data.code).first()
    if existing_rule_table:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Rule table with code '{rule_table_data.code}' already exists"
        )
    
    # 创建规则表
    rule_table = RuleTable(
        id=str(uuid4()),
        code=rule_table_data.code,
        name=rule_table_data.name,
        file_type=rule_table_data.file_type,
        rule_stage=rule_table_data.rule_stage,
        enabled=rule_table_data.enabled,
        description=rule_table_data.description
    )
    
    db.add(rule_table)
    db.commit()
    db.refresh(rule_table)
    
    return GeneralResponse(data=RuleTableResponse.from_orm(rule_table))

# 获取规则表详情
@router.get("/{id}", response_model=GeneralResponse[RuleTableResponse], tags=["rule-tables"])
async def get_rule_table(
    id: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    rule_table = db.query(RuleTable).filter(RuleTable.id == id).first()
    if not rule_table:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Rule table with id '{id}' not found"
        )
    
    return GeneralResponse(data=RuleTableResponse.from_orm(rule_table))

# 更新规则表
@router.put("/{id}", response_model=GeneralResponse[RuleTableResponse], tags=["rule-tables"])
async def update_rule_table(
    id: str,
    rule_table_data: RuleTableUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    rule_table = db.query(RuleTable).filter(RuleTable.id == id).first()
    if not rule_table:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Rule table with id '{id}' not found"
        )
    
    # 更新字段
    update_data = rule_table_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(rule_table, field, value)
    
    db.commit()
    db.refresh(rule_table)
    
    return GeneralResponse(data=RuleTableResponse.from_orm(rule_table))

# 删除规则表
@router.delete("/{id}", response_model=GeneralResponse[dict], tags=["rule-tables"])
async def delete_rule_table(
    id: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    rule_table = db.query(RuleTable).filter(RuleTable.id == id).first()
    if not rule_table:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Rule table with id '{id}' not found"
        )
    
    db.delete(rule_table)
    db.commit()
    
    return GeneralResponse(data={"message": f"Rule table '{rule_table.name}' deleted successfully"})

# 启用规则表
@router.put("/{id}/enable", response_model=GeneralResponse[RuleTableResponse], tags=["rule-tables"])
async def enable_rule_table(
    id: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    rule_table = db.query(RuleTable).filter(RuleTable.id == id).first()
    if not rule_table:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Rule table with id '{id}' not found"
        )
    
    rule_table.enabled = True
    db.commit()
    db.refresh(rule_table)
    
    return GeneralResponse(data=RuleTableResponse.from_orm(rule_table))

# 禁用规则表
@router.put("/{id}/disable", response_model=GeneralResponse[RuleTableResponse], tags=["rule-tables"])
async def disable_rule_table(
    id: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    rule_table = db.query(RuleTable).filter(RuleTable.id == id).first()
    if not rule_table:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Rule table with id '{id}' not found"
        )
    
    rule_table.enabled = False
    db.commit()
    db.refresh(rule_table)
    
    return GeneralResponse(data=RuleTableResponse.from_orm(rule_table))
