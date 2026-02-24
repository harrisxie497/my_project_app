"""修复Y列的规则配置"""
import sys
import os
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# 初始化数据库连接
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env'))
database_url = os.getenv('DATABASE_URL')
engine = create_engine(database_url)

# 更新Y列的规则配置
conn = engine.connect()

# 查看Y列当前的配置
print("Y列当前配置：")
result = conn.execute(text("""
    SELECT target_col, target_header, source_cols, rule_ref, depends_on, field_type, enabled
    FROM field_pipelines
    WHERE target_col = 'Y' AND file_type = 'CUSTOMS'
"""))

for row in result:
    print(f"  target_col: {row[0]}")
    print(f"  target_header: {row[1]}")
    print(f"  source_cols: {row[2]}")
    print(f"  rule_ref: {row[3]}")
    print(f"  depends_on: {row[4]}")
    print(f"  field_type: {row[5]}")
    print(f"  enabled: {row[6]}")

# 更新Y列的规则为 policy_ai_text_dress_clean
print("\n更新Y列的规则配置...")
conn.execute(text("""
    UPDATE field_pipelines
    SET rule_ref = '["policy_ai_text_dress_clean"]',
        field_type = 'AI'
    WHERE target_col = 'Y' AND file_type = 'CUSTOMS'
"""))

conn.commit()

# 查看更新后的配置
print("\nY列更新后的配置：")
result = conn.execute(text("""
    SELECT target_col, target_header, source_cols, rule_ref, depends_on, field_type, enabled
    FROM field_pipelines
    WHERE target_col = 'Y' AND file_type = 'CUSTOMS'
"""))

for row in result:
    print(f"  target_col: {row[0]}")
    print(f"  target_header: {row[1]}")
    print(f"  source_cols: {row[2]}")
    print(f"  rule_ref: {row[3]}")
    print(f"  depends_on: {row[4]}")
    print(f"  field_type: {row[5]}")
    print(f"  enabled: {row[6]}")

conn.close()

print("\nY列规则配置更新完成！")
