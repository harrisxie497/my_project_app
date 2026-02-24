#!/usr/bin/env python3
"""
测试所有AI字段（F列改为保留一位小数，使用处理后的H列和I列）
"""

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

# 测试数据（3行）
test_data = [
    {'H': '飞轮玩具(12-24M)', 'I': 'ABS(100%)', 'F': '1.234', 'X': '田中 太郎', 'Y': '東京都渋谷区渋谷1-2-3', 'J': '山田 太郎', 'K': '東京都渋谷区渋谷1-2-3'},
    {'H': 'T恤(L码)', 'I': '棉(100%)', 'F': '2.567', 'X': '鈴木 花子', 'Y': '大阪府大阪市中央区1-2-3', 'J': '田中 花子', 'K': '大阪府大阪市中央区1-2-3'},
    {'H': '连衣裙(XL码)', 'I': '涤纶(100%)', 'F': '0.890', 'X': '佐藤 一郎', 'Y': '愛知県名古屋市中区1-2-3', 'J': '鈴木 一郎', 'K': '愛知県名古屋市中区1-2-3'}
]

# 字段配置（F列需要使用处理后的H列和I列）
field_configs = [
    {'target_col': 'H', 'rule_ref': 'policy_ai_goods_en', 'target_header': '品名'},
    {'target_col': 'I', 'rule_ref': 'policy_ai_material_en', 'target_header': '材质'},
    {'target_col': 'F', 'rule_ref': 'policy_ai_decimal_fix', 'target_header': '货物重量'},
    {'target_col': 'X', 'rule_ref': 'policy_ai_text_ja_clean', 'target_header': '收件人名'},
    {'target_col': 'Y', 'rule_ref': 'policy_ai_text_dress_clean', 'target_header': '收件人地址'},
    {'target_col': 'J', 'rule_ref': 'policy_translate_from_targetcol_en_upper', 'target_header': '輸入者名'},
    {'target_col': 'K', 'rule_ref': 'policy_ai_text_dress_clean', 'target_header': '輸入者住所'}
]

# 获取规则配置
conn = engine.connect()

print("=" * 80)
print("AI字段测试（F列保留一位小数，J/K列移除序号）")
print("=" * 80)

results = []
processed_data = {}  # 存储已处理的数据
total_start_time = time.time()

# 先处理H列和I列（F列需要它们的处理结果）
for field_config in field_configs:
    if field_config['target_col'] not in ['H', 'I']:
        continue

    target_col = field_config['target_col']
    rule_ref = field_config['rule_ref']
    target_header = field_config['target_header']

    print(f"\n字段 {target_col}列 ({target_header}) - 先处理（F列需要）")
    print("-" * 80)

    # 获取规则配置
    result = conn.execute(text("""
        SELECT schema_json
        FROM rule_definitions
        WHERE rule_ref = :rule_ref
    """), {'rule_ref': rule_ref})

    row = result.fetchone()
    if not row:
        print(f"规则 '{rule_ref}' 未找到，跳过")
        continue

    schema = json.loads(row[0])
    system_prompt = schema.get('configurable_params', {}).get('system_prompt')
    desc = schema.get('desc')

    # 构建用户提示词
    col_list = [row[target_col] for row in test_data]
    user_prompt = f"{desc}\n\n{chr(10).join([f'{i+1}. {v}' for i, v in enumerate(col_list)])}\n\n要求：\n1. 输入的数组顺序保持不变\n2. 每行一个结果，按顺序对应\n3. 只返回结果，不要包含序号"

    start_time = time.time()
    try:
        ai_result = ai_service.chat(user_prompt, system_prompt=system_prompt)
        elapsed_time = time.time() - start_time

        # 调试：打印原始AI返回结果
        print(f"\n[DEBUG] AI原始返回结果：")
        print(f"'{ai_result}'")
        print(f"长度: {len(ai_result)}")
        for i, char in enumerate(ai_result):
            print(f"  char[{i}] = '{char}' (ord={ord(char)})")

        # 解析结果并移除序号
        lines = ai_result.strip().split('\n')
        cleaned_results = []
        for line in lines:
            line = line.strip()
            if line:
                parts = line.split('.')
                if len(parts) > 1 and parts[0].strip().isdigit():
                    cleaned_results.append('.'.join(parts[1:]).strip())
                else:
                    cleaned_results.append(line)

        # 调试：打印解析后的结果
        print(f"\n[DEBUG] 解析后的结果：")
        print(f"{cleaned_results}")

        # 存储处理结果
        processed_data[target_col] = cleaned_results
        results.append({
            'col': target_col,
            'header': target_header,
            'input': col_list,
            'output': cleaned_results,
            'time': elapsed_time
        })

        print(f"\nAI返回结果（耗时{elapsed_time:.2f}秒）：")
        for i, (inp, out) in enumerate(zip(col_list, cleaned_results), 1):
            print(f"  {i}. {inp} -> {out}")

    except Exception as e:
        print(f"\n处理失败: {e}")
        processed_data[target_col] = col_list  # 使用原始值
        results.append({
            'col': target_col,
            'header': target_header,
            'input': col_list,
            'output': col_list,
            'time': 0,
            'error': str(e)
        })

# 处理其他字段
for idx, field_config in enumerate(field_configs, 1):
    target_col = field_config['target_col']
    rule_ref = field_config['rule_ref']
    target_header = field_config['target_header']

    if target_col in ['H', 'I']:
        continue

    print(f"\n字段 {len([r for r in results if r['col'] in ['H', 'I']]) + idx}/{len(field_configs)}: {target_col}列 ({target_header})")
    print("-" * 80)

    # 获取规则配置
    result = conn.execute(text("""
        SELECT schema_json
        FROM rule_definitions
        WHERE rule_ref = :rule_ref
    """), {'rule_ref': rule_ref})

    row = result.fetchone()
    if not row:
        print(f"规则 '{rule_ref}' 未找到，跳过")
        continue

    schema = json.loads(row[0])
    system_prompt = schema.get('configurable_params', {}).get('system_prompt')
    desc = schema.get('desc')

    # 构建用户提示词
    user_prompt = f"{desc}\n\n"

    if target_col == 'F':
        # F列特殊处理：使用已处理的H列和I列
        h_list = processed_data.get('H', [row['H'] for row in test_data])
        i_list = processed_data.get('I', [row['I'] for row in test_data])
        f_list = [row['F'] for row in test_data]

        user_prompt += f"材质数组：\n{chr(10).join(i_list)}\n\n"
        user_prompt += f"品名数组：\n{chr(10).join(h_list)}\n\n"
        user_prompt += f"重量数组：\n{chr(10).join(f_list)}\n\n"
        user_prompt += "要求：\n"
        user_prompt += "1. 输入的数组顺序保持不变\n"
        user_prompt += "2. 每行一个结果，按顺序对应，只返回重量数值\n"
        user_prompt += "3. 必须保留完整数值并四舍五入到一位小数（例如：1.234kg->1.2，2.567kg->2.6，0.890kg->0.9）\n"
        user_prompt += "4. 绝对不要提取小数位单独返回（如2、6、9），必须返回完整的一位小数数值（如1.2、2.6、0.9）\n"
        user_prompt += "5. 只返回结果，不要包含序号、单位或其他文字"

        print(f"用户提示词:\n{user_prompt}")
    else:
        # 其他字段：简单列表
        col_list = [row[target_col] for row in test_data]
        user_prompt += f"{chr(10).join([f'{i+1}. {v}' for i, v in enumerate(col_list)])}\n\n"
        user_prompt += "要求：\n"
        user_prompt += "1. 输入的数组顺序保持不变\n"
        user_prompt += "2. 每行一个结果，按顺序对应\n"
        user_prompt += "3. 只返回结果，不要包含序号"

    start_time = time.time()
    try:
        ai_result = ai_service.chat(user_prompt, system_prompt=system_prompt)
        elapsed_time = time.time() - start_time

        # 调试：打印原始AI返回结果
        print(f"\n[DEBUG] AI原始返回结果：")
        print(f"'{ai_result}'")
        print(f"长度: {len(ai_result)}")
        for i, char in enumerate(ai_result):
            print(f"  char[{i}] = '{char}' (ord={ord(char)})")

        # 解析结果并移除序号
        lines = ai_result.strip().split('\n')
        cleaned_results = []
        for line in lines:
            line = line.strip()
            if line:
                parts = line.split('.')
                if len(parts) > 1 and parts[0].strip().isdigit():
                    cleaned_results.append('.'.join(parts[1:]).strip())
                else:
                    cleaned_results.append(line)

        # 调试：打印解析后的结果
        print(f"\n[DEBUG] 解析后的结果：")
        print(f"{cleaned_results}")

        results.append({
            'col': target_col,
            'header': target_header,
            'input': [row[target_col] for row in test_data],
            'output': cleaned_results,
            'time': elapsed_time
        })

        print(f"\nAI返回结果（耗时{elapsed_time:.2f}秒）：")
        for i, (inp, out) in enumerate(zip([row[target_col] for row in test_data], cleaned_results), 1):
            print(f"  {i}. {inp} -> {out}")

    except Exception as e:
        print(f"\n处理失败: {e}")
        results.append({
            'col': target_col,
            'header': target_header,
            'input': [row[target_col] for row in test_data],
            'output': [],
            'time': 0,
            'error': str(e)
        })

conn.close()

total_time = time.time() - total_start_time

# 输出总结
print("\n" + "=" * 80)
print("测试总结")
print("=" * 80)

print(f"\n配置的字段数：{len(field_configs)}")
print(f"处理成功的字段：{len([r for r in results if r.get('output')])}")
print(f"跳过的字段：{len([r for r in results if not r.get('output')])}")
print(f"每条数据：{len(test_data)}行")
print(f"总耗时：{total_time:.2f}秒")
print(f"平均每字段：{total_time/len(field_configs):.2f}秒")
print(f"API调用次数：{len(field_configs)}次（每列一次）")

print("\n详细结果：")
for r in results:
    print(f"\n{r['col']}列 ({r['header']}):")
    if r.get('output'):
        print(f"  输入: {r['input']}")
        print(f"  输出: {r['output']}")
        print(f"  耗时: {r['time']:.2f}秒")
    else:
        print(f"  失败: {r.get('error', 'Unknown error')}")

# F列特别验证
f_result = next((r for r in results if r['col'] == 'F'), None)
if f_result:
    expected_f = [str(round(float(row['F']), 1)) for row in test_data]
    print(f"\nF列验证（一位小数）：")
    print(f"  期望: {expected_f}")
    print(f"  实际: {f_result['output']}")
    if f_result['output'] == expected_f:
        print(f"  [通过]")
    else:
        print(f"  [失败]")
