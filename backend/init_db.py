from sqlalchemy.orm import Session
from uuid import uuid4
from app.core.database import SessionLocal, engine, Base
from app.models.user import User
from app.core.auth import get_password_hash

# 创建所有数据库表
Base.metadata.create_all(bind=engine)

# 创建数据库会话
db = SessionLocal()

try:
    # 删除已存在的管理员用户（如果有），以便重新创建
    db.query(User).filter(User.username == "admin").delete()
    db.commit()
    
    # 使用新的密码哈希算法创建管理员用户
    admin_user = User(
        id=f"u_{uuid4().hex[:8]}",
        username="admin",
        display_name="管理员",
        hashed_password=get_password_hash("admin123"),
        role="admin"
    )
    db.add(admin_user)
    db.commit()
    print("默认管理员用户创建成功")
    print(f"用户名: {admin_user.username}")
    print(f"密码: admin123")
    print(f"角色: {admin_user.role}")
        
except Exception as e:
    print(f"创建管理员用户失败: {e}")
    db.rollback()
finally:
    db.close()
