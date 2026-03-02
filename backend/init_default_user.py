"""
初始化默认用户
"""
import sys
import os
import logging
from datetime import datetime, timedelta

# 添加项目路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.core.database import SessionLocal
from app.models.user import User
from app.core.auth import get_password_hash

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def init_default_user():
    """
    初始化默认用户
    """
    logger.info("开始初始化默认用户...")

    db = SessionLocal()
    try:
        # 检查是否已存在管理员用户
        existing_user = db.query(User).filter(User.username == "admin").first()
        
        if existing_user:
            logger.info("管理员用户已存在，跳过创建")
            return existing_user

        # 创建默认管理员用户
        admin_user = User(
            username="admin",
            email="admin@example.com",
            hashed_password=get_password_hash("admin123"),
            full_name="系统管理员",
            is_active=True,
            is_superuser=True
        )
        
        db.add(admin_user)
        db.commit()
        db.refresh(admin_user)
        
        logger.info(f"默认管理员用户创建成功！")
        logger.info(f"用户名: {admin_user.username}")
        logger.info(f"邮箱: {admin_user.email}")
        logger.info(f"密码: admin123")
        logger.info(f"请尽快修改默认密码！")
        
        return admin_user

    except Exception as e:
        logger.error(f"创建默认用户失败: {str(e)}", exc_info=True)
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    init_default_user()
    logger.info("默认用户初始化完成")
