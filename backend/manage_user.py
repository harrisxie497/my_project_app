"""
查看和重置用户密码
"""
import sys
import os
import logging

# 添加项目路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.core.database import SessionLocal
from app.models.user import User
from app.core.auth import get_password_hash, verify_password

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def list_users():
    """
    列出所有用户
    """
    logger.info("开始查询用户...")
    
    db = SessionLocal()
    try:
        users = db.query(User).all()
        
        if not users:
            logger.info("数据库中没有用户")
            return
        
        logger.info(f"找到 {len(users)} 个用户：")
        for user in users:
            logger.info(f"  - 用户名: {user.username}")
            logger.info(f"    显示名: {user.display_name}")
            logger.info(f"    角色: {user.role}")
            logger.info(f"    是否启用: {user.enabled}")
        
    except Exception as e:
        logger.error(f"查询用户失败: {str(e)}", exc_info=True)
    finally:
        db.close()


def reset_user_password(username: str, new_password: str):
    """
    重置用户密码
    """
    logger.info(f"开始重置用户 {username} 的密码...")
    
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.username == username).first()
        
        if not user:
            logger.error(f"用户 {username} 不存在")
            return False
        
        # 更新密码
        user.hashed_password = get_password_hash(new_password)
        db.commit()
        
        logger.info(f"用户 {username} 的密码已重置")
        logger.info(f"新密码: {new_password}")
        
        return True
        
    except Exception as e:
        logger.error(f"重置密码失败: {str(e)}", exc_info=True)
        db.rollback()
        return False
    finally:
        db.close()


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="用户管理工具")
    parser.add_argument("--list", action="store_true", help="列出所有用户")
    parser.add_argument("--reset", type=str, help="重置指定用户的密码")
    parser.add_argument("--password", type=str, default="admin123", help="新密码（默认：admin123）")
    
    args = parser.parse_args()
    
    if args.list:
        list_users()
    elif args.reset:
        success = reset_user_password(args.reset, args.password)
        if success:
            logger.info("密码重置成功")
        else:
            logger.error("密码重置失败")
    else:
        parser.print_help()
