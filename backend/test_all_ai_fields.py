"""测试所有AI处理类型的字段"""
import sys
import os
import json
import time
from dotenv import load_dotenv

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine, text
from app.services.deepseek_ai_service import DeepSeekAIService

def get_all_ai_fields(engine, file_type):
    """
    获取所有AI类型的字段配置

    输入：
        - engine: 数据库引擎
        - file_type: 文件类型

    输出：
        - AI字段配置列表
    """
    conn = engine.connect()
    result = conn.execute(text("""
        SELECT target_col, target_header, source_cols, rule_ref, depends_on
        FROM field_pipelines
        WHERE file_type = :file_type
          AND field_type = 'AI'
          AND enabled = 1
        ORDER BY order_num
    """), {"file_type": file_type})

    fields = []
    for row in result:
        # row[0]: target_col
        # row[1]: target_header
        # row[2]: source_cols
        # row[3]: rule_ref
        # row[4]: depends_on
        rule_refs = json.loads(row[3]) if row[3] else []
        fields.append({
            'target_col': row[0],
            'target_header': row[1],
            'source_cols': json.loads(row[2]) if row[2] else [],
            'depends_on': json.loads(row[4]) if row[4] else [],
            'rule_ref': rule_refs[0] if rule_refs else None
        })

    conn.close()
    return fields

def get_rule_config(engine, rule_ref):
    """
    获取规则配置

    输入：
        - engine: 数据库引擎
        - rule_ref: 规则引用

    输出：
        - 规则配置字典
    """
    conn = engine.connect()
    result = conn.execute(text("""
        SELECT schema_json
        FROM rule_definitions
        WHERE rule_ref = :rule_ref
    """), {"rule_ref": rule_ref})

    row = result.fetchone()
    if not row:
        conn.close()
        return None

    schema = json.loads(row[0])
    conn.close()

    return {
        'desc': schema.get('desc'),
        'handler': schema.get('handler'),
        'system_prompt': schema.get('configurable_params', {}).get('system_prompt')
    }

def execute_ai_field(ai_service, field_config, rule_config, test_data):
    """
    执行AI字段处理

    输入：
        - ai_service: AI服务实例
        - field_config: 字段配置
        - rule_config: 规则配置
        - test_data: 测试数据列表

    输出：
        - 处理结果
    """
    system_prompt = rule_config.get('system_prompt')

    # 构建输入项
    input_items = []
    for row_data in test_data:
        for col in field_config['source_cols']:
            value = row_data.get(col, '')
            input_items.append({'col': col, 'value': value})

    # 构建用户提示词
    items_text = []
    for idx, item in enumerate(input_items):
        items_text.append(f"{idx+1}. {item['col']}: {item['value']}")

    user_prompt = f"""{rule_config.get('desc', '')}

{chr(10).join(items_text)}

要求：
1. 输入的数组顺序保持不变
2. 每行一个结果，按顺序对应
3. 只返回结果，不要包含其他文字"""

    # 调用AI
    start_time = time.time()
    result = ai_service.chat(user_prompt, system_prompt=system_prompt)
    elapsed_time = time.time() - start_time

    # 解析结果
    lines = result.strip().split('\n')
    results = [line.strip() for line in lines if line.strip()]

    # 确保结果数量匹配
    while len(results) < len(test_data):
        results.append('')

    return results[:len(test_data)], elapsed_time

def test_all_ai_fields():
    """测试所有AI处理类型的字段"""
    print("=" * 80)
    print("测试所有AI处理类型的字段")
    print("=" * 80)

    # 初始化数据库连接
    load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env'))
    database_url = os.getenv('DATABASE_URL')
    engine = create_engine(database_url)

    # 初始化AI服务
    api_key = os.getenv('DEEPSEEK_API_KEY')
    ai_service = DeepSeekAIService(api_key=api_key)

    # 获取所有AI字段配置
    print("\n1. 获取所有AI字段配置")
    print("-" * 80)
    ai_fields = get_all_ai_fields(engine, 'CUSTOMS')

    print(f"找到 {len(ai_fields)} 个AI字段：")
    for i, field in enumerate(ai_fields, 1):
        print(f"\n{i}. 目标列: {field['target_col']} ({field['target_header']})")
        print(f"   源列: {field['source_cols']}")
        print(f"   依赖列: {field['depends_on']}")
        print(f"   规则: {field['rule_ref']}")

    # 准备测试数据
    print("\n2. 准备测试数据")
    print("-" * 80)

    test_data = [
        {
            "F": "1.234",
            "H": "AIRPLANE TOY (L码)",
            "I": "cotton (100%)",
            "AD": "山田 太郎 様"
        },
        {
            "F": "2.567",
            "H": "T-SHIRT (XL) blue",
            "I": "polyster (blend)",
            "AD": "田中 花子 様方"
        },
        {
            "F": "0.890",
            "H": "SHOES (Size 42)",
            "I": "leather (Genuine)",
            "AD": "鈴木 一郎 先生"
        }
    ]

    print("测试数据（3条）：")
    for i, row in enumerate(test_data, 1):
        print(f"\n{i}. F(重量): {row['F']}")
        print(f"   H(品名): {row['H']}")
        print(f"   I(材质): {row['I']}")
        print(f"   AD(收件人): {row['AD']}")

    # 测试每个AI字段
    print("\n3. 执行AI字段处理")
    print("=" * 80)

    total_time = 0
    total_fields = len(ai_fields)

    for field_idx, field_config in enumerate(ai_fields, 1):
        print(f"\n{'=' * 80}")
        print(f"字段 {field_idx}/{total_fields}: {field_config['target_col']} - {field_config['target_header']}")
        print("=" * 80)

        # 获取规则配置
        rule_config = get_rule_config(engine, field_config['rule_ref'])

        if not rule_config:
            print(f"\n[SKIP] 规则 {field_config['rule_ref']} 未找到配置")
            total_fields -= 1
            continue

        print(f"\n规则描述: {rule_config.get('desc')}")
        print(f"处理器: {rule_config.get('handler')}")
        print(f"系统提示词: {rule_config.get('system_prompt')[:50]}..." if rule_config.get('system_prompt') and len(rule_config.get('system_prompt')) > 50 else f"系统提示词: {rule_config.get('system_prompt')}")

        # 执行处理
        try:
            results, elapsed_time = execute_ai_field(
                ai_service=ai_service,
                field_config=field_config,
                rule_config=rule_config,
                test_data=test_data
            )

            total_time += elapsed_time

            print(f"\n处理完成！耗时: {elapsed_time:.2f}秒")
            print(f"\n输入 -> 输出：")

            for i, (input_row, result) in enumerate(zip(test_data, results), 1):
                input_value = input_row.get(field_config['source_cols'][0], '') if field_config['source_cols'] else ''
                output_value = result if result else '[ERROR]'

                print(f"{i}. 输入: {input_value}")
                print(f"   输出: {output_value}")
                print()

        except Exception as e:
            print(f"\n[ERROR] 处理失败: {str(e)}")
            import traceback
            traceback.print_exc()

    # 总结
    print("\n" + "=" * 80)
    print("测试总结")
    print("=" * 80)
    print(f"测试字段数: {total_fields}")
    print(f"每条数据: {len(test_data)} 行")
    print(f"总耗时: {total_time:.2f}秒")
    print(f"平均每字段: {total_time/total_fields:.2f}秒")
    print(f"API调用次数: {total_fields} 次（每列一次）")
    print("=" * 80)

if __name__ == "__main__":
    test_all_ai_fields()
