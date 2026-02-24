"""检查field_pipelines表结构和AI规则配置"""
import sys
import os
import json
from dotenv import load_dotenv

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine, text

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env'))

database_url = os.getenv('DATABASE_URL')
engine = create_engine(database_url)
conn = engine.connect()

# 查看表结构
print("=" * 80)
print("field_pipelines表结构")
print("=" * 80)
result = conn.execute(text('DESCRIBE field_pipelines'))
for row in result:
    print(f"{row[0]:30} {row[1]:20}")

# 查询所有列名
result = conn.execute(text("""
    SELECT column_name, data_type
    FROM information_schema.columns
    WHERE table_name = 'field_pipelines'
    ORDER BY ordinal_position
"""))
print("\n字段索引：")
for i, row in enumerate(result):
    print(f"{i}: {row[0]:30} {row[1]:20}")

# 查询包含AI规则的pipeline
print("\n" + "=" * 80)
print("包含AI规则的field_pipelines")
print("=" * 80)
result = conn.execute(text("""
    SELECT * FROM field_pipelines
    WHERE JSON_SEARCH(rule_ref, 'one', 'policy_ai%') IS NOT NULL
    LIMIT 5
"""))

rows = result.fetchall()
columns = result.keys()

for row in rows:
    print(f"\n完整数据行：")
    for i, (key, value) in enumerate(zip(columns, row)):
        print(f"  [{i}] {key}: {value}")

conn.close()

