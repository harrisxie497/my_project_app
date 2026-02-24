"""更新F列的系统提示词"""
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

# 更新policy_ai_decimal_fix的系统提示词
new_system_prompt = """输入的数组数据是'材质'，'品名'，'货物重量'，我们依据数组中同位置的"材料"和"品名"来判断"货物重量"是否合理？ 如果合理，我们保留两位小数（如"1.234"→"1.23"，"2.567"→"2.57"，"0.890"→"0.89"），如果觉得不合理，判定为异常值（如明显偏离合理范围的数值），则可以虚拟一个合理数字，注意这个重量是一件商品的重量，单位KG，对于输出的要求，也是一个数组，并且顺序和数组长度保持输入的一样。"""

print("更新F列的系统提示词...")
print(f"\n新的系统提示词：\n{new_system_prompt}\n")

# 获取当前的schema_json
conn = engine.connect()
result = conn.execute(text("""
    SELECT schema_json
    FROM rule_definitions
    WHERE rule_ref = 'policy_ai_decimal_fix'
"""))

row = result.fetchone()
if not row:
    print("错误：未找到policy_ai_decimal_fix规则")
    conn.close()
    sys.exit(1)

schema = json.loads(row[0])

# 更新系统提示词
schema['configurable_params']['system_prompt'] = new_system_prompt

# 更新数据库
conn.execute(text("""
    UPDATE rule_definitions
    SET schema_json = :schema_json,
        updated_at = NOW()
    WHERE rule_ref = 'policy_ai_decimal_fix'
"""), {"schema_json": json.dumps(schema, ensure_ascii=False)})

conn.commit()
conn.close()

print("系统提示词更新成功！")

# 验证更新
conn = engine.connect()
result = conn.execute(text("""
    SELECT schema_json
    FROM rule_definitions
    WHERE rule_ref = 'policy_ai_decimal_fix'
"""))

row = result.fetchone()
schema = json.loads(row[0])
updated_prompt = schema['configurable_params']['system_prompt']

print(f"\n验证更新后的系统提示词：\n{updated_prompt[:100]}...")
conn.close()
