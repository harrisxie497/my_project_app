from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from uuid import uuid4
from typing import Optional, List
from app.core.auth import get_current_active_user, get_password_hash
from app.core.config import settings
from app.core.database import get_db
from app.models.user import User
from app.schemas.user import (
    UserCreate, UserUpdate, UserResponse, PaginatedUserList
)
from app.schemas.response import GeneralResponse
from app.utils.operation_log import log_operation

router = APIRouter(redirect_slashes=False)
admin_router = APIRouter(redirect_slashes=False)

# 获取用户列表
@router.get("/", response_model=GeneralResponse[PaginatedUserList], tags=["users"])
async def get_users(
    username: Optional[str] = Query(None, description="用户名搜索"),
    role: Optional[str] = Query(None, description="角色过滤"),
    enabled: Optional[bool] = Query(None, description="是否启用过滤"),
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页条数"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    # 构建查询
    query = db.query(User)
    
    # 应用过滤条件
    if username:
        query = query.filter(User.username.contains(username))
    if role:
        query = query.filter(User.role == role)
    if enabled is not None:
        query = query.filter(User.enabled == enabled)
    
    # 计算总数
    total = query.count()
    
    # 应用分页
    skip = (page - 1) * page_size
    users = query.order_by(User.created_at.desc()).offset(skip).limit(page_size).all()
    
    # 转换为响应模型
    user_list = [UserResponse.from_orm(user) for user in users]
    
    return GeneralResponse(
        data=PaginatedUserList(
            items=user_list,
            page=page,
            page_size=page_size,
            total=total
        )
    )

# 创建用户
@router.post("/", response_model=GeneralResponse[UserResponse], tags=["users"])
async def create_user(
    user_data: UserCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    # 检查用户名是否已存在
    existing_user = db.query(User).filter(User.username == user_data.username).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"User with username '{user_data.username}' already exists"
        )
    
    # 创建用户
    hashed_password = get_password_hash(user_data.password)
    user = User(
        id=str(uuid4()),
        username=user_data.username,
        display_name=user_data.display_name,
        hashed_password=hashed_password,
        role=user_data.role,
        enabled=user_data.enabled
    )
    
    db.add(user)
    db.commit()
    db.refresh(user)
    
    # 记录创建用户日志
    log_operation(
        db=db,
        user_id=current_user.id,
        action="USER_CREATED",
        entity_type="user",
        entity_id=user.id,
        success=True,
        message=f"User '{user.username}' created successfully",
        detail_json={"username": user.username, "role": user.role, "created_by": current_user.username}
    )
    
    return GeneralResponse(data=UserResponse.from_orm(user))

# 获取用户详情
@router.get("/{id}", response_model=GeneralResponse[UserResponse], tags=["users"])
async def get_user(
    id: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id '{id}' not found"
        )
    
    return GeneralResponse(data=UserResponse.from_orm(user))

# 更新用户信息
@router.put("/{id}", response_model=GeneralResponse[UserResponse], tags=["users"])
async def update_user(
    id: str,
    user_data: UserUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id '{id}' not found"
        )
    
    # 更新字段
    update_data = user_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(user, field, value)
    
    db.commit()
    db.refresh(user)
    
    # 记录更新用户日志
    log_operation(
        db=db,
        user_id=current_user.id,
        action="USER_UPDATED",
        entity_type="user",
        entity_id=user.id,
        success=True,
        message=f"User '{user.username}' updated successfully",
        detail_json={"username": user.username, "updated_fields": list(update_data.keys()), "updated_by": current_user.username}
    )
    
    return GeneralResponse(data=UserResponse.from_orm(user))

# 删除用户
@router.delete("/{id}", response_model=GeneralResponse[dict], tags=["users"])
async def delete_user(
    id: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id '{id}' not found"
        )
    
    username = user.username
    db.delete(user)
    db.commit()
    
    # 记录删除用户日志
    log_operation(
        db=db,
        user_id=current_user.id,
        action="USER_DELETED",
        entity_type="user",
        entity_id=id,
        success=True,
        message=f"User '{username}' deleted successfully",
        detail_json={"username": username, "deleted_by": current_user.username}
    )
    
    return GeneralResponse(data={"message": f"User '{username}' deleted successfully"})

# 启用用户
@router.put("/{id}/enable", response_model=GeneralResponse[UserResponse], tags=["users"])
async def enable_user(
    id: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id '{id}' not found"
        )
    
    user.enabled = True
    db.commit()
    db.refresh(user)
    
    # 记录启用用户日志
    log_operation(
        db=db,
        user_id=current_user.id,
        action="USER_ENABLED",
        entity_type="user",
        entity_id=user.id,
        success=True,
        message=f"User '{user.username}' enabled successfully",
        detail_json={"username": user.username, "enabled_by": current_user.username}
    )
    
    return GeneralResponse(data=UserResponse.from_orm(user))

# 禁用用户
@router.put("/{id}/disable", response_model=GeneralResponse[UserResponse], tags=["users"])
async def disable_user(
    id: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id '{id}' not found"
        )
    
    user.enabled = False
    db.commit()
    db.refresh(user)
    
    # 记录禁用用户日志
    log_operation(
        db=db,
        user_id=current_user.id,
        action="USER_DISABLED",
        entity_type="user",
        entity_id=user.id,
        success=True,
        message=f"User '{user.username}' disabled successfully",
        detail_json={"username": user.username, "disabled_by": current_user.username}
    )
    
    return GeneralResponse(data=UserResponse.from_orm(user))

# 管理员获取用户列表
@admin_router.get("/", response_model=GeneralResponse[List[UserResponse]], tags=["admin-users"])
async def admin_get_users(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    # 管理员可以获取所有用户
    users = db.query(User).order_by(User.created_at.desc()).all()
    
    # 转换为响应模型
    user_list = [UserResponse.from_orm(user) for user in users]
    
    return GeneralResponse(data=user_list)

# 管理员创建用户
@admin_router.post("/", response_model=GeneralResponse[dict], tags=["admin-users"])
async def admin_create_user(
    user_data: UserCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    # 检查用户名是否已存在
    existing_user = db.query(User).filter(User.username == user_data.username).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"User with username '{user_data.username}' already exists"
        )
    
    # 创建用户
    hashed_password = get_password_hash(user_data.password)
    user = User(
        id=str(uuid4()),
        username=user_data.username,
        display_name=user_data.display_name,
        hashed_password=hashed_password,
        role=user_data.role,
        enabled=user_data.enabled
    )
    
    db.add(user)
    db.commit()
    db.refresh(user)
    
    # 记录管理员创建用户日志
    log_operation(
        db=db,
        user_id=current_user.id,
        action="ADMIN_USER_CREATED",
        entity_type="user",
        entity_id=user.id,
        success=True,
        message=f"Admin created user '{user.username}'",
        detail_json={"username": user.username, "role": user.role, "created_by": current_user.username, "created_by_role": current_user.role}
    )
    
    return GeneralResponse(data={"id": user.id})

# 管理员启用/禁用用户
@admin_router.put("/{id}", response_model=GeneralResponse[dict], tags=["admin-users"])
async def admin_enable_disable_user(
    id: str,
    enabled: bool = Query(..., description="是否启用用户"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id '{id}' not found"
        )
    
    old_status = user.enabled
    user.enabled = enabled
    db.commit()
    db.refresh(user)
    
    # 记录管理员启用/禁用用户日志
    action = "ADMIN_USER_ENABLED" if enabled else "ADMIN_USER_DISABLED"
    log_operation(
        db=db,
        user_id=current_user.id,
        action=action,
        entity_type="user",
        entity_id=user.id,
        success=True,
        message=f"Admin {'enabled' if enabled else 'disabled'} user '{user.username}'",
        detail_json={"username": user.username, "old_status": old_status, "new_status": enabled, "admin": current_user.username}
    )
    
    return GeneralResponse(data={"id": user.id, "enabled": user.enabled})

# 管理员重置用户密码
@admin_router.post("/{id}/reset-password", response_model=GeneralResponse[dict], tags=["admin-users"])
async def admin_reset_password(
    id: str,
    request: dict,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    # 获取请求体中的新密码
    new_password = request.get("new_password")
    if not new_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="new_password is required"
        )
    
    user = db.query(User).filter(User.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id '{id}' not found"
        )
    
    # 更新密码
    user.hashed_password = get_password_hash(new_password)
    db.commit()
    
    # 记录管理员重置密码日志
    log_operation(
        db=db,
        user_id=current_user.id,
        action="ADMIN_PASSWORD_RESET",
        entity_type="user",
        entity_id=user.id,
        success=True,
        message=f"Admin reset password for user '{user.username}'",
        detail_json={"username": user.username, "admin": current_user.username}
    )
    
    return GeneralResponse(data={"message": f"Password for user '{user.username}' reset successfully"})
