from pydantic_settings import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
    # 应用配置
    APP_NAME: str = "日本清关Excel自动生成系统"
    API_V1_STR: str = "/api/v1"
    DEBUG: bool = True
    
    # 数据库配置
    DATABASE_URL: str = "mysql+pymysql://app:app123456@172.18.207.224:3306/demo?charset=utf8mb4"
    
    # JWT配置
    SECRET_KEY: str = "wwRfvTJQMOGRHELw5QmmSULPwVg5zBEeR9CbyfMTVeY"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # 文件存储配置
    STORAGE_PATH: str = os.path.join(os.getcwd(), "storage")
    TASKS_STORAGE_PATH: str = os.path.join(STORAGE_PATH, "tasks")
    
    class Config:
        env_file = ".env"
        case_sensitive = True

# 创建全局配置实例
settings = Settings()

# 确保存储目录存在
os.makedirs(settings.TASKS_STORAGE_PATH, exist_ok=True)
