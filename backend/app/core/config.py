from pydantic_settings import BaseSettings
from typing import Optional
import os
from pathlib import Path

class Settings(BaseSettings):
    # 应用配置
    APP_NAME: str = "日本清关Excel自动生成系统"
    API_V1_STR: str = "/api/v1"
    DEBUG: bool = False
    
    # 数据库配置 - 使用SQLite数据库避免依赖外部MySQL服务器
    DATABASE_URL: str = "sqlite:///./test.db"
    
    # JWT配置
    SECRET_KEY: str = "wwRfvTJQMOGRHELw5QmmSULPwVg5zBEeR9CbyfMTVeY"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # DeepSeek AI配置
    DEEPSEEK_API_KEY: str = ""
    DEEPSEEK_API_URL: str = "https://api.deepseek.com/v1"
    
    # 汇率API配置
    EXCHANGE_RATE_API_KEY: str = ""
    EXCHANGE_RATE_API_URL: str = "https://v6.exchangerate-api.com/v6"
    
    # 文件存储配置
    STORAGE_PATH: str = os.path.join(os.getcwd(), "storage")
    TASKS_STORAGE_PATH: str = os.path.join(STORAGE_PATH, "tasks")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True
        extra = "ignore"

# 创建全局配置实例
settings = Settings()

# 确保存储目录存在
os.makedirs(settings.TASKS_STORAGE_PATH, exist_ok=True)
