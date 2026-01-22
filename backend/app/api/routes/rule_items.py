from fastapi import APIRouter, Depends, HTTPException, status, Query, UploadFile, File
from sqlalchemy.orm import Session
from uuid import uuid4
from typing import Optional, List
from app.core.auth import get_current_active_user
from app.core.config import settings
from app.core.database import get_db
from app.models.user import User
from app.models.rule_item import RuleItem
from app.models.rule_table import RuleTable
from app.schemas.rule_item import (
    RuleItemCreate, RuleItemUpdate, RuleItemResponse, PaginatedRuleItemList
)
from app.schemas.response import GeneralResponse

router = APIRouter(redirect_slashes=False)
admin_router = APIRouter(redirect_slashes=False)

# 获取规则项列表
@router.get("/", response_model=GeneralResponse[PaginatedRuleItemList], tags=["rule-items"])
async def get_rule_items(
    rule_table_id: Optional[str] = Query(None, description="规则表ID过滤"),
    enabled: Optional[bool] = Query(None, description="是否启用过滤"),
    target_column: Optional[str] = Query(None, description="目标列搜索"),
    field_type: Optional[str] = Query(None, description="字段类型过滤"),
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页条数"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    # 构建查询
    query = db.query(RuleItem)
    
    # 应用过滤条件
    if rule_table_id:
        query = query.filter(RuleItem.rule_table_id == rule_table_id)
    if enabled is not None:
        query = query.filter(RuleItem.enabled == enabled)
    if target_column:
        query = query.filter(RuleItem.target_column == target_column)
    if field_type:
        query = query.filter(RuleItem.field_type == field_type)
    
    # 计算总数
    total = query.count()
    
    # 应用分页
    skip = (page - 1) * page_size
    rule_items = query.order_by(RuleItem.order_no, RuleItem.created_at.desc()).offset(skip).limit(page_size).all()
    
    # 转换为响应模型
    rule_item_list = [RuleItemResponse.from_orm(ri) for ri in rule_items]
    
    return GeneralResponse(
        data=PaginatedRuleItemList(
            items=rule_item_list,
            page=page,
            page_size=page_size,
            total=total
        )
    )

# 创建规则项
@router.post("/", response_model=GeneralResponse[RuleItemResponse], tags=["rule-items"])
async def create_rule_item(
    rule_item_data: RuleItemCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    # 检查规则表是否存在
    rule_table = db.query(RuleTable).filter(RuleTable.id == rule_item_data.rule_table_id).first()
    if not rule_table:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Rule table with id '{rule_item_data.rule_table_id}' not found"
        )
    
    # 创建规则项
    rule_item = RuleItem(
        id=str(uuid4()),
        rule_table_id=rule_item_data.rule_table_id,
        enabled=rule_item_data.enabled,
        order_no=rule_item_data.order_no,
        target_column=rule_item_data.target_column,
        target_field_name=rule_item_data.target_field_name,
        map_op=rule_item_data.map_op,
        source_column=rule_item_data.source_column,
        field_type=rule_item_data.field_type,
        process_depends_on=rule_item_data.process_depends_on,
        process_rules_json=rule_item_data.process_rules_json,
        executor=rule_item_data.executor,
        on_fail=rule_item_data.on_fail,
        note=rule_item_data.note
    )
    
    db.add(rule_item)
    db.commit()
    db.refresh(rule_item)
    
    return GeneralResponse(data=RuleItemResponse.from_orm(rule_item))

# 获取规则项详情
@router.get("/{id}", response_model=GeneralResponse[RuleItemResponse], tags=["rule-items"])
async def get_rule_item(
    id: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    rule_item = db.query(RuleItem).filter(RuleItem.id == id).first()
    if not rule_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Rule item with id '{id}' not found"
        )
    
    return GeneralResponse(data=RuleItemResponse.from_orm(rule_item))

# 更新规则项
@router.put("/{id}", response_model=GeneralResponse[RuleItemResponse], tags=["rule-items"])
async def update_rule_item(
    id: str,
    rule_item_data: RuleItemUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    rule_item = db.query(RuleItem).filter(RuleItem.id == id).first()
    if not rule_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Rule item with id '{id}' not found"
        )
    
    # 更新字段
    update_data = rule_item_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(rule_item, field, value)
    
    db.commit()
    db.refresh(rule_item)
    
    return GeneralResponse(data=RuleItemResponse.from_orm(rule_item))

# 删除规则项
@router.delete("/{id}", response_model=GeneralResponse[dict], tags=["rule-items"])
async def delete_rule_item(
    id: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    rule_item = db.query(RuleItem).filter(RuleItem.id == id).first()
    if not rule_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Rule item with id '{id}' not found"
        )
    
    db.delete(rule_item)
    db.commit()
    
    return GeneralResponse(data={"message": f"Rule item for column '{rule_item.target_column}' deleted successfully"})

# 启用规则项
@router.put("/{id}/enable", response_model=GeneralResponse[RuleItemResponse], tags=["rule-items"])
async def enable_rule_item(
    id: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    rule_item = db.query(RuleItem).filter(RuleItem.id == id).first()
    if not rule_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Rule item with id '{id}' not found"
        )
    
    rule_item.enabled = True
    db.commit()
    db.refresh(rule_item)
    
    return GeneralResponse(data=RuleItemResponse.from_orm(rule_item))

# 禁用规则项
@router.put("/{id}/disable", response_model=GeneralResponse[RuleItemResponse], tags=["rule-items"])
async def disable_rule_item(
    id: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    rule_item = db.query(RuleItem).filter(RuleItem.id == id).first()
    if not rule_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Rule item with id '{id}' not found"
        )
    
    rule_item.enabled = False
    db.commit()
    db.refresh(rule_item)
    
    return GeneralResponse(data=RuleItemResponse.from_orm(rule_item))

# 获取指定规则表的规则项
@router.get("/rule-table/{rule_table_id}", response_model=GeneralResponse[List[RuleItemResponse]], tags=["rule-items"])
async def get_rule_items_by_table(
    rule_table_id: str,
    enabled: Optional[bool] = Query(None, description="是否启用过滤"),
    target_column: Optional[str] = Query(None, description="目标列搜索"),
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
    
    # 构建查询
    query = db.query(RuleItem).filter(RuleItem.rule_table_id == rule_table_id)
    
    # 应用过滤条件
    if enabled is not None:
        query = query.filter(RuleItem.enabled == enabled)
    if target_column:
        query = query.filter(RuleItem.target_column == target_column)
    
    # 获取规则项
    rule_items = query.order_by(RuleItem.order_no).all()
    
    # 转换为响应模型
    rule_item_list = [RuleItemResponse.from_orm(ri) for ri in rule_items]
    
    return GeneralResponse(data=rule_item_list)

# 规则导入接口（非管理员版本，保持向后兼容）
@router.post("/import", response_model=GeneralResponse[dict], tags=["rule-items"])
async def import_rules(
    file: UploadFile = File(..., description="规则导入Excel文件"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    # 验证文件类型
    if not file.filename.endswith(".xlsx"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only .xlsx files are allowed"
        )
    
    # 这里可以添加规则导入的具体实现逻辑
    # 例如：解析Excel文件，批量创建规则表和规则项
    
    # 目前返回模拟数据
    result = {
        "imported": {"rule_tables": 4, "rule_items": 120},
        "updated": {"rule_tables": 0, "rule_items": 12},
        "skipped": 3,
        "warnings": ["PROCESS_CUSTOMS: target_column B duplicated, kept latest"]
    }
    
    return GeneralResponse(data=result)

# 管理员规则导入接口（符合API设计文档路径）
@admin_router.post("/import", response_model=GeneralResponse[dict], tags=["admin-rules"])
async def admin_import_rules(
    file: UploadFile = File(..., description="规则导入Excel文件"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    # 验证文件类型
    if not file.filename.endswith(".xlsx"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only .xlsx files are allowed"
        )
    
    # 这里可以添加规则导入的具体实现逻辑
    # 例如：解析Excel文件，批量创建规则表和规则项
    
    # 目前返回模拟数据
    result = {
        "imported": {"rule_tables": 4, "rule_items": 120},
        "updated": {"rule_tables": 0, "rule_items": 12},
        "skipped": 3,
        "warnings": ["PROCESS_CUSTOMS: target_column B duplicated, kept latest"]
    }
    
    return GeneralResponse(data=result)
