from sqlalchemy import inspect
from app.core.database import engine

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

print("\n数据库检查完成!")
