from datetime import timedelta, datetime
from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from uuid import uuid4
from app.core.auth import authenticate_user, create_access_token, get_current_active_user, get_user, verify_password
from app.core.config import settings
from app.core.database import get_db
from app.models.user import User
from app.schemas.user import UserLogin, Token, UserResponse
from app.schemas.response import GeneralResponse
from app.utils.operation_log import log_operation

router = APIRouter(redirect_slashes=False)

# 登录接口
@router.post("/login", response_model=GeneralResponse[Token], tags=["auth"])
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    # 先检查用户是否存在
    user = get_user(db, form_data.username)
    if not user:
        # 记录登录失败日志
        log_operation(
            db=db,
            user_id="unknown",
            action="LOGIN_FAILED",
            entity_type="user",
            success=False,
            message=f"User with username '{form_data.username}' does not exist",
            detail_json={"username": form_data.username}
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User does not exist",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 检查用户是否被禁用
    if not user.enabled:
        # 记录登录失败日志
        log_operation(
            db=db,
            user_id=user.id,
            action="LOGIN_FAILED",
            entity_type="user",
            entity_id=user.id,
            success=False,
            message="User account is disabled",
            detail_json={"username": form_data.username}
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User account is disabled",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 检查密码是否正确
    if not verify_password(form_data.password, user.hashed_password):
        # 记录登录失败日志
        log_operation(
            db=db,
            user_id=user.id,
            action="LOGIN_FAILED",
            entity_type="user",
            entity_id=user.id,
            success=False,
            message="Incorrect password",
            detail_json={"username": form_data.username}
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 更新用户最后登录时间
    user.last_login_at = datetime.utcnow()
    db.commit()
    
    # 记录登录成功日志
    log_operation(
        db=db,
        user_id=user.id,
        action="LOGIN_SUCCESS",
        entity_type="user",
        entity_id=user.id,
        success=True,
        message="User logged in successfully",
        detail_json={"username": form_data.username}
    )
    
    # 创建访问令牌
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=access_token_expires
    )
    
    return GeneralResponse(
        data=Token(
            access_token=access_token,
            token_type="bearer",
            user=UserResponse.from_orm(user)
        )
    )

# 获取当前用户信息
@router.get("/me", response_model=GeneralResponse[UserResponse], tags=["auth"])
async def get_me(
    current_user: User = Depends(get_current_active_user)
):
    return GeneralResponse(data=UserResponse.from_orm(current_user))

# 登出接口（JWT模式下主要由前端删除令牌）
@router.post("/logout", response_model=GeneralResponse[dict], tags=["auth"])
async def logout(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    # 记录登出日志
    log_operation(
        db=db,
        user_id=current_user.id,
        action="LOGOUT",
        entity_type="user",
        entity_id=current_user.id,
        success=True,
        message="User logged out successfully",
        detail_json={"username": current_user.username}
    )
    
    # 在JWT模式下，这里可以实现令牌黑名单功能
    return GeneralResponse(data={"message": "Successfully logged out"})
