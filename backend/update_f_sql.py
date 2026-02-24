#!/usr/bin/env python3
import sys
import os
import json
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env'))
database_url = os.getenv('DATABASE_URL')
engine = create_engine(database_url)

conn = engine.connect()

# 新的schema
new_schema = {
    "desc": "重量：按品名/材质/原重量进行合理修正，输出一位小数（后台固定流程）",
    "handler": "ai.decimal_fix",
    "configurable_params": {
        "system_prompt": """输入的数组数据是'材质'，'品名'，'货物重量'，我们依据数组中同位置的"材料"和"品名"来判断"货物重量"是否合理？如果合理，保留完整数值并四舍五入到一位小数（例如：输入1.234返回1.2，输入2.567返回2.6，输入0.890返回0.9），如果觉得不合理，判定为异常值（如明显偏离合理范围的数值），则可以虚拟一个合理数字，注意这个重量是一件商品的重量，单位KG，对于输出的要求，也是一个数组，并且顺序和数组长度保持输入的一样。重要说明：返回完整的一位小数数值，不要单独提取小数位。"""
    }
}

# 执行更新
result = conn.execute(text("""
    UPDATE rule_definitions
    SET schema_json = :schema_json
    WHERE rule_ref = 'policy_ai_decimal_fix'
"""), {'schema_json': json.dumps(new_schema, ensure_ascii=False)})

conn.commit()

print(f"Updated {result.rowcount} rows")

# 验证更新
result = conn.execute(text("""
    SELECT schema_json
    FROM rule_definitions
    WHERE rule_ref = 'policy_ai_decimal_fix'
"""))

row = result.fetchone()
schema = json.loads(row[0])
print("\nVerified schema:")
print(json.dumps(schema, indent=2, ensure_ascii=False))

conn.close()
