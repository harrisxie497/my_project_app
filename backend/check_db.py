from sqlalchemy import inspect, select
from app.core.database import engine, SessionLocal
from app.models.user import User

# 创建数据库检查器
inspector = inspect(engine)

# 检查数据库类型
print(f"数据库URL: {engine.url}")

# 获取所有表名
tables = inspector.get_table_names()
print(f"\n数据库中存在的表: {tables}")

# 检查users表
if 'users' in tables:
    print("\n✓ users表已创建")
    columns = inspector.get_columns('users')
    print("users表字段:")
    for column in columns:
        print(f"  - {column['name']} ({column['type']})")
    
    # 查询用户数据
    db = SessionLocal()
    try:
        users = db.query(User).all()
        print("\n用户列表:")
        for user in users:
            print(f"  - 用户名: {user.username}, 显示名称: {user.display_name}, 角色: {user.role}, 启用状态: {user.enabled}")
    finally:
        db.close()
else:
    print("\n✗ users表未创建")

# 检查tasks表
if 'tasks' in tables:
    print("\n✓ tasks表已创建")
    columns = inspector.get_columns('tasks')
    print("tasks表字段:")
    for column in columns:
        print(f"  - {column['name']} ({column['type']})")
else:
    print("\n✗ tasks表未创建")

# 检查file_definitions表
if 'file_definitions' in tables:
    print("\n✓ file_definitions表已创建")
    columns = inspector.get_columns('file_definitions')
    print("file_definitions表字段:")
    for column in columns:
        print(f"  - {column['name']} ({column['type']})")
    
    # 查询file_definitions数据
    from app.models.file_definition import FileDefinition
    db = SessionLocal()
    try:
        file_definitions = db.query(FileDefinition).all()
        print(f"\n文件定义数量: {len(file_definitions)}")
        for fd in file_definitions:
            print(f"  - ID: {fd.id}, 文件类型: {fd.file_type}, 文件角色: {fd.file_role}, 启用状态: {fd.enabled}")
    finally:
        db.close()
else:
    print("\n✗ file_definitions表未创建")

print("\n数据库检查完成!")
