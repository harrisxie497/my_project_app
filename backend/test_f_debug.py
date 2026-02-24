"""调试F列的处理"""
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

# 测试1：带序号的三个数组（当前的测试脚本方式）
print("\n测试1：带序号的三个数组")
print("=" * 80)

user_prompt1 = f"""你是一个物流数据处理专家。请分析以下货物信息，修复重量数据的小数点问题。

材质数组：
1. cotton (100%)
2. polyster (blend)
3. leather (Genuine)

品名数组：
1. AIRPLANE TOY (L码)
2. T-SHIRT (XL) blue
3. SHOES (Size 42)

重量数组：
1. 1.234
2. 2.567
3. 0.890

要求：
1. 输入的数组顺序保持不变
2. 每行一个结果，按顺序对应，只返回重量数值
3. 保留两位小数（例如：1.234 → 1.23，2.567 → 2.57，0.890 → 0.89）
4. 只返回结果，不要包含序号、单位或其他文字"""

print(f"\n用户提示词：\n{user_prompt1}")

start_time = time.time()
result1 = ai_service.chat(user_prompt1, system_prompt=system_prompt)
elapsed1 = time.time() - start_time

print(f"\nAI返回结果（耗时{elapsed1:.2f}秒）：")
print(result1)

# 测试2：不带序号的三个数组
print("\n" + "=" * 80)
print("测试2：不带序号的三个数组")
print("=" * 80)

user_prompt2 = f"""你是一个物流数据处理专家。请分析以下货物信息，修复重量数据的小数点问题。

材质数组：
cotton (100%)
polyster (blend)
leather (Genuine)

品名数组：
AIRPLANE TOY (L码)
T-SHIRT (XL) blue
SHOES (Size 42)

重量数组：
1.234
2.567
0.890

要求：
1. 输入的数组顺序保持不变
2. 每行一个结果，按顺序对应，只返回重量数值
3. 保留两位小数（例如：1.234 → 1.23，2.567 → 2.57，0.890 → 0.89）
4. 只返回结果，不要包含序号、单位或其他文字"""

print(f"\n用户提示词：\n{user_prompt2}")

start_time = time.time()
result2 = ai_service.chat(user_prompt2, system_prompt=system_prompt)
elapsed2 = time.time() - start_time

print(f"\nAI返回结果（耗时{elapsed2:.2f}秒）：")
print(result2)

# 测试3：逐行格式（AI执行器的方式）
print("\n" + "=" * 80)
print("测试3：逐行格式")
print("=" * 80)

user_prompt3 = f"""你是一个物流数据处理专家。请分析以下货物信息，修复重量数据的小数点问题。

1. 材质：cotton (100%)，品名：AIRPLANE TOY (L码)，重量：1.234
2. 材质：polyster (blend)，品名：T-SHIRT (XL) blue，重量：2.567
3. 材质：leather (Genuine)，品名：SHOES (Size 42)，重量：0.890

要求：
1. 输入的数组顺序保持不变
2. 每行一个结果，按顺序对应，只返回重量数值
3. 保留两位小数（例如：1.234 → 1.23，2.567 → 2.57，0.890 → 0.89）
4. 只返回结果，不要包含序号、单位或其他文字"""

print(f"\n用户提示词：\n{user_prompt3}")

start_time = time.time()
result3 = ai_service.chat(user_prompt3, system_prompt=system_prompt)
elapsed3 = time.time() - start_time

print(f"\nAI返回结果（耗时{elapsed3:.2f}秒）：")
print(result3)

# 总结
print("\n" + "=" * 80)
print("对比总结")
print("=" * 80)
print(f"\n期望结果：")
print("  1.23")
print("  2.57")
print("  0.89")

print(f"\n测试1（带序号的三个数组）：")
print(result1)

print(f"\n测试2（不带序号的三个数组）：")
print(result2)

print(f"\n测试3（逐行格式）：")
print(result3)
