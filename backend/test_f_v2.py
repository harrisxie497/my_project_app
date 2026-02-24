"""测试F列（V2系统提示词）"""
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

print("F列规则描述：")
print(desc)
print("\nF列系统提示词：")
print(system_prompt)
print("\n" + "=" * 80)

# 测试数据
test_data = [
    {
        "F": "1.234",
        "H": "AIRPLANE TOY (L码)",
        "I": "cotton (100%)"
    },
    {
        "F": "2.567",
        "H": "T-SHIRT (XL) blue",
        "I": "polyster (blend)"
    },
    {
        "F": "0.890",
        "H": "SHOES (Size 42)",
        "I": "leather (Genuine)"
    }
]

# 构建材质、品名、重量数组
material_list = [row['I'] for row in test_data]
goods_list = [row['H'] for row in test_data]
weight_list = [row['F'] for row in test_data]

# 构建用户提示词
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
3. 保留完整数值并四舍五入到两位小数，例如：输入1.234返回1.23，输入2.567返回2.57，输入0.890返回0.89
4. 绝对不要提取小数位单独返回（如23、57、89），而是返回完整的两位小数数值
5. 只返回结果，不要包含序号、单位或其他文字"""

print("\n用户提示词：")
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

print(f"\n期望结果：")
for i, row in enumerate(test_data, 1):
    original = float(row['F'])
    expected = round(original, 2)
    print(f"  {i}. {expected}")
