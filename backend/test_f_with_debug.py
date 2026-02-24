"""测试F列并打印提示词"""
import sys
import os
import json
import time
from dotenv import load_dotenv

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine, text
from app.services.deepseek_ai_service import DeepSeekAIService

# 初始化数据库连接
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env'))
database_url = os.getenv('DATABASE_URL')
engine = create_engine(database_url)

# 初始化AI服务
api_key = os.getenv('DEEPSEEK_API_KEY')
ai_service = DeepSeekAIService(api_key=api_key)

# 测试数据（模拟处理后的H和I）
test_data = [
    {
        "F": "1.234",
        "H": "AIRPLANE TOY",
        "I": "COTTON"
    },
    {
        "F": "2.567",
        "H": "T-SHIRT BLUE",
        "I": "POLYESTER"
    },
    {
        "F": "0.890",
        "H": "SHOES",
        "I": "LEATHER"
    }
]

# 获取F列的规则配置
conn = engine.connect()
result = conn.execute(text("""
    SELECT schema_json
    FROM rule_definitions
    WHERE rule_ref = 'policy_ai_decimal_fix'
"""))

row = result.fetchone()
schema = json.loads(row[0])
system_prompt = schema.get('configurable_params', {}).get('system_prompt')
desc = schema.get('desc')
conn.close()

print("规则描述：")
print(desc)
print("\n系统提示词：")
print(system_prompt)
print("\n" + "=" * 80)

# 构建材质、品名、重量数组（不带序号）
material_list = [row['I'] for row in test_data]
goods_list = [row['H'] for row in test_data]
weight_list = [row['F'] for row in test_data]

print("\n材质数组：")
for i, v in enumerate(material_list, 1):
    print(f"  {i}. {v}")

print("\n品名数组：")
for i, v in enumerate(goods_list, 1):
    print(f"  {i}. {v}")

print("\n重量数组：")
for i, v in enumerate(weight_list, 1):
    print(f"  {i}. {v}")

# 构建用户提示词（不带序号）
user_prompt = f"""{desc}

材质数组：
{chr(10).join(material_list)}

品名数组：
{chr(10).join(goods_list)}

重量数组：
{chr(10).join(weight_list)}

要求：
1. 输入的数组顺序保持不变
2. 每行一个结果，按顺序对应，只返回重量数值
3. 保留两位小数（例如：1.234 → 1.23，2.567 → 2.57，0.890 → 0.89）
4. 只返回结果，不要包含序号、单位或其他文字"""

print("\n" + "=" * 80)
print("用户提示词：")
print("=" * 80)
print(user_prompt)

print("\n" + "=" * 80)
print("调用AI...")
print("=" * 80)

start_time = time.time()
result = ai_service.chat(user_prompt, system_prompt=system_prompt)
elapsed_time = time.time() - start_time

print(f"\nAI返回结果（耗时{elapsed_time:.2f}秒）：")
print(result)

# 解析结果
lines = result.strip().split('\n')
results = [line.strip() for line in lines if line.strip()]

print(f"\n解析后：")
for i, r in enumerate(results, 1):
    print(f"  {i}. {r}")
