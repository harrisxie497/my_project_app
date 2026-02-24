import logging
import os
from logging.handlers import RotatingFileHandler
from app.core.config import settings


def setup_logging():
    """
    配置应用日志系统
    
    创建两个日志文件：
    - app.log: 应用主日志，记录应用级别的信息
    - api.log: API接口日志，记录API请求和响应
    
    日志格式：时间戳 - 模块名 - 级别 - 消息
    日志轮转：10MB文件大小，保留5个备份
    
    :return: None
    """
    # 确保日志目录存在
    log_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "logs")
    os.makedirs(log_dir, exist_ok=True)
    
    # 定义日志格式
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    date_format = "%Y-%m-%d %H:%M:%S"
    
    # 配置根日志记录器
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO if not settings.DEBUG else logging.DEBUG)
    
    # 清除现有的处理器
    root_logger.handlers.clear()
    
    # 创建控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG if settings.DEBUG else logging.INFO)
    console_formatter = logging.Formatter(log_format, date_format)
    console_handler.setFormatter(console_formatter)
    root_logger.addHandler(console_handler)
    
    # 创建应用主日志文件处理器
    app_log_file = os.path.join(log_dir, "app.log")
    app_file_handler = RotatingFileHandler(
        app_log_file,
        maxBytes=10 * 1024 * 1024,  # 10MB
        backupCount=5,
        encoding='utf-8'
    )
    app_file_handler.setLevel(logging.DEBUG if settings.DEBUG else logging.INFO)
    app_file_formatter = logging.Formatter(log_format, date_format)
    app_file_handler.setFormatter(app_file_formatter)
    root_logger.addHandler(app_file_handler)
    
    # 创建API日志文件处理器
    api_log_file = os.path.join(log_dir, "api.log")
    api_file_handler = RotatingFileHandler(
        api_log_file,
        maxBytes=10 * 1024 * 1024,  # 10MB
        backupCount=5,
        encoding='utf-8'
    )
    api_file_handler.setLevel(logging.DEBUG if settings.DEBUG else logging.INFO)
    api_file_formatter = logging.Formatter(log_format, date_format)
    api_file_handler.setFormatter(api_file_formatter)
    root_logger.addHandler(api_file_handler)
    
    # 为API模块创建专门的日志记录器
    api_logger = logging.getLogger("app.api")
    api_logger.addHandler(api_file_handler)
    api_logger.propagate = False
    
    # 记录日志系统初始化完成
    root_logger.info(f"日志系统初始化完成 - 日志目录: {log_dir}")


def get_logger(name: str) -> logging.Logger:
    """
    获取指定名称的日志记录器
    
    :param name: 日志记录器名称，通常使用模块名（如 __name__）
    :return: 日志记录器实例
    """
    return logging.getLogger(name)
