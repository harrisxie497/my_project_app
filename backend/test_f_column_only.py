"""专门测试F列的处理"""
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

# 测试数据
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
conn.close()

print("F列系统提示词：")
print(system_prompt)
print("\n" + "=" * 80)

# 构建材质、品名、重量数组
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

# 方法1：原来的方式（只提供重量）
print("\n" + "=" * 80)
print("方法1：只提供重量数组")
print("=" * 80)

user_prompt1 = f"""你是一个物流数据处理专家。请分析以下货物信息，修复重量数据的小数点问题。

重量数组：
{chr(10).join([f"{i+1}. {v}" for i, v in enumerate(weight_list)])}

要求：
1. 输入的数组顺序保持不变
2. 每行一个结果，按顺序对应
3. 保留两位小数
4. 只返回数值，不要包含单位或其他文字"""

print(f"\n用户提示词：\n{user_prompt1}")

start_time = time.time()
result1 = ai_service.chat(user_prompt1, system_prompt=system_prompt)
elapsed1 = time.time() - start_time

print(f"\nAI返回结果（耗时{elapsed1:.2f}秒）：")
print(result1)

lines = result1.strip().split('\n')
results1 = [line.strip() for line in lines if line.strip()]
print(f"\n解析后：")
for i, r in enumerate(results1, 1):
    print(f"  {i}. {r}")

# 方法2：提供完整的三组数组
print("\n" + "=" * 80)
print("方法2：提供材质、品名、重量三组数组")
print("=" * 80)

user_prompt2 = f"""你是一个物流数据处理专家。请分析以下货物信息，修复重量数据的小数点问题。

材质数组：
{chr(10).join([f"{i+1}. {v}" for i, v in enumerate(material_list)])}

品名数组：
{chr(10).join([f"{i+1}. {v}" for i, v in enumerate(goods_list)])}

重量数组：
{chr(10).join([f"{i+1}. {v}" for i, v in enumerate(weight_list)])}

要求：
1. 输入的数组顺序保持不变
2. 每行一个结果，按顺序对应
3. 保留两位小数
4. 只返回数值，不要包含单位或其他文字"""

print(f"\n用户提示词：\n{user_prompt2}")

start_time = time.time()
result2 = ai_service.chat(user_prompt2, system_prompt=system_prompt)
elapsed2 = time.time() - start_time

print(f"\nAI返回结果（耗时{elapsed2:.2f}秒）：")
print(result2)

lines = result2.strip().split('\n')
results2 = [line.strip() for line in lines if line.strip()]
print(f"\n解析后：")
for i, r in enumerate(results2, 1):
    print(f"  {i}. {r}")

# 方法3：逐个处理（明确说明保留小数位）
print("\n" + "=" * 80)
print("方法3：逐个处理并明确说明保留小数位")
print("=" * 80)

user_prompt3_items = []
for i in range(len(test_data)):
    user_prompt3_items.append(
        f"{i+1}. 材质：{material_list[i]}，品名：{goods_list[i]}，重量：{weight_list[i]}，"
    )

user_prompt3 = f"""你是一个物流数据处理专家。请分析以下货物信息，修复重量数据的小数点问题。

{chr(10).join(user_prompt3_items)}

要求：
1. 输入的数组顺序保持不变
2. 每行一个结果，按顺序对应
3. 保留两位小数（例如：1.234 → 1.23，2.567 → 2.57，0.890 → 0.89）
4. 只返回数值，不要包含单位或其他文字
5. 不要提取小数位单独返回，而是返回完整的两位小数数值"""

print(f"\n用户提示词：\n{user_prompt3}")

start_time = time.time()
result3 = ai_service.chat(user_prompt3, system_prompt=system_prompt)
elapsed3 = time.time() - start_time

print(f"\nAI返回结果（耗时{elapsed3:.2f}秒）：")
print(result3)

lines = result3.strip().split('\n')
results3 = [line.strip() for line in lines if line.strip()]
print(f"\n解析后：")
for i, r in enumerate(results3, 1):
    print(f"  {i}. {r}")

# 对比总结
print("\n" + "=" * 80)
print("三种方法对比")
print("=" * 80)
print(f"\n输入：")
for i, row in enumerate(test_data, 1):
    print(f"  {i}. {row['F']}")

print(f"\n方法1（只提供重量）：")
for i, r in enumerate(results1, 1):
    print(f"  {i}. {r}")

print(f"\n方法2（提供三组数组）：")
for i, r in enumerate(results2, 1):
    print(f"  {i}. {r}")

print(f"\n方法3（逐个处理+明确说明）：")
for i, r in enumerate(results3, 1):
    print(f"  {i}. {r}")

print(f"\n期望结果：")
for i, row in enumerate(test_data, 1):
    # 简单四舍五入到两位小数
    original = float(row['F'])
    expected = round(original, 2)
    print(f"  {i}. {expected}")
