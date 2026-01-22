from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

# 用户基础信息
class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    display_name: str = Field(..., min_length=1, max_length=100)
    role: str = Field(default="user", pattern="^(admin|user|operator)$")

# 创建用户请求
class UserCreate(UserBase):
    password: str = Field(..., min_length=6, max_length=50)

# 更新用户请求
class UserUpdate(BaseModel):
    display_name: Optional[str] = Field(None, min_length=1, max_length=100)
    enabled: Optional[bool] = None
    role: Optional[str] = Field(None, pattern="^(admin|user|operator)$")

# 用户登录请求
class UserLogin(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6, max_length=50)

# 用户响应
class UserResponse(UserBase):
    id: str
    enabled: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    last_login_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

# 登录响应
class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse

# 分页用户列表响应
class PaginatedUserList(BaseModel):
    items: list[UserResponse]
    page: int
    page_size: int
    total: int
