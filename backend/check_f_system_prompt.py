"""检查F列的系统提示词"""
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

# 获取F列的规则配置
conn = engine.connect()
result = conn.execute(text("""
    SELECT rule_ref, schema_json
    FROM rule_definitions
    WHERE rule_ref = 'policy_ai_decimal_fix'
"""))

row = result.fetchone()
schema = json.loads(row[1])
system_prompt = schema.get('configurable_params', {}).get('system_prompt')

print("=" * 80)
print("F列系统提示词（完整）：")
print("=" * 80)
print(system_prompt)
print("=" * 80)

conn.close()
