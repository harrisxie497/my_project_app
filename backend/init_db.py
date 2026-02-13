"""
初始化数据库 - 创建所有表
"""
import sys
import os
import logging

# 添加项目路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.core.database import Base, engine
from app.models import user, task, field_pipeline, rule_definition, file_definition, excel_config

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def init_db():
    """
    初始化数据库：创建所有表
    """
    logger.info("开始初始化数据库...")
    logger.info(f"数据库URL: {engine.url}")

    try:
        # 创建所有表
        Base.metadata.create_all(bind=engine)
        logger.info("数据库表创建成功！")

        # 列出所有表
        tables = Base.metadata.tables.keys()
        logger.info(f"已创建的表: {', '.join(tables)}")

    except Exception as e:
        logger.error(f"数据库初始化失败: {str(e)}", exc_info=True)
        raise


if __name__ == "__main__":
    init_db()
    logger.info("数据库初始化完成")
