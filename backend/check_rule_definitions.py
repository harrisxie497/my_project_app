"""检查rule_definitions表中的AI规则配置"""
import sys
import os
import json
from dotenv import load_dotenv

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine, text

# 直接读取.env文件
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env'))

database_url = os.getenv('DATABASE_URL')
print(f"DATABASE_URL: {database_url[:50]}...")

engine = create_engine(database_url)
conn = engine.connect()

# 先查看表结构
print("\n" + "=" * 80)
print("rule_definitions表结构")
print("=" * 80)
result = conn.execute(text('DESCRIBE rule_definitions'))
for row in result:
    print(f"{row[0]:30} {row[1]:20} {row[2] if len(row) > 2 else ''}")

# 查询所有规则
print("\n" + "=" * 80)
print("所有规则配置")
print("=" * 80)
result = conn.execute(text('SELECT * FROM rule_definitions LIMIT 5'))
rows = result.fetchall()
print(f"总列数: {len(rows[0]) if rows else 0}")
print(f"列名: {result.keys()}")

# 查询AI规则
print("\n" + "=" * 80)
print("AI规则配置")
print("=" * 80)
result = conn.execute(text("""
    SELECT * FROM rule_definitions
    WHERE rule_ref LIKE 'policy_ai%'
    ORDER BY rule_ref
"""))

for row in result:
    print(f"\n规则ID: {row[0]}")
    print(f"规则引用: {row[1]}")
    print(f"规则名称: {row[2]}")
    print(f"规则描述: {row[3]}")
    # 检查所有列
    keys = result.keys()
    for i, key in enumerate(keys):
        if i < len(row):
            print(f"{key}: {row[i]}")

conn.close()

