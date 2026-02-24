"""测试从数据库读取配置并执行AI规则处理"""
import sys
import os
import json
from dotenv import load_dotenv

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine, text
from app.services.deepseek_ai_service import DeepSeekAIService

def get_rule_config_from_db(engine, rule_ref):
    """
    从数据库获取规则配置

    输入：
        - engine: 数据库引擎
        - rule_ref: 规则引用

    输出：
        - system_prompt: 系统提示词
        - handler: 处理器名称
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
        return None, None

    schema = json.loads(row[0])
    config_params = schema.get('configurable_params', {})
    system_prompt = config_params.get('system_prompt')
    handler = schema.get('handler')

    conn.close()
    return system_prompt, handler

def get_field_pipeline_config(engine, file_type, target_col):
    """
    从数据库获取字段pipeline配置

    输入：
        - engine: 数据库引擎
        - file_type: 文件类型
        - target_col: 目标列

    输出：
        - source_cols: 源列列表
        - depends_on: 依赖列列表
        - rule_ref: 规则引用
    """
    conn = engine.connect()
    result = conn.execute(text("""
        SELECT source_cols, depends_on, rule_ref
        FROM field_pipelines
        WHERE file_type = :file_type
          AND target_col = :target_col
          AND enabled = 1
        LIMIT 1
    """), {"file_type": file_type, "target_col": target_col})

    row = result.fetchone()
    if not row:
        conn.close()
        return None, None, None

    source_cols = json.loads(row[0]) if row[0] else []
    depends_on = json.loads(row[2]) if row[2] else []
    rule_refs = json.loads(row[1]) if row[1] else []
    rule_ref = rule_refs[0] if rule_refs else None

    conn.close()
    return source_cols, depends_on, rule_ref

def execute_ai_rule_batch(ai_service, system_prompt, input_items, output_format=""):
    """
    批量执行AI规则

    输入：
        - ai_service: AI服务实例
        - system_prompt: 系统提示词
        - input_items: 输入项列表 [{"col": 列名, "value": 值}, ...]
        - output_format: 输出格式要求

    输出：
        - 结果列表
    """
    # 构建输入文本
    items_text = []
    for idx, item in enumerate(input_items):
        col = item.get('col', '')
        value = item.get('value', '')
        items_text.append(f"{idx+1}. {col}: {value}")

    # 构建用户提示词
    user_prompt = f"""请处理以下数据：

{chr(10).join(items_text)}

{output_format}

每行一个结果，按顺序对应，只返回结果，不要包含其他文字。"""

    # 调用AI服务
    result = ai_service.chat(user_prompt, system_prompt=system_prompt)

    # 解析结果
    lines = result.strip().split('\n')
    results = [line.strip() for line in lines if line.strip()]

    return results

def test_h_column_from_db():
    """测试从数据库配置处理H列"""
    print("=" * 80)
    print("测试从数据库读取配置并处理H列（英文品名清理）")
    print("=" * 80)

    # 初始化数据库连接
    load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env'))
    database_url = os.getenv('DATABASE_URL')
    engine = create_engine(database_url)

    # 初始化AI服务
    api_key = os.getenv('DEEPSEEK_API_KEY')
    ai_service = DeepSeekAIService(api_key=api_key)

    # 获取H列的配置
    print("\n1. 获取H列配置")
    print("-" * 80)
    source_cols, depends_on, rule_ref = get_field_pipeline_config(
        engine, 'CUSTOMS', 'H'
    )

    print(f"源列 (source_cols): {source_cols}")
    print(f"依赖列 (depends_on): {depends_on}")
    print(f"规则引用 (rule_ref): {rule_ref}")

    # 获取规则定义
    print("\n2. 获取规则定义")
    print("-" * 80)
    system_prompt, handler = get_rule_config_from_db(engine, rule_ref)

    print(f"处理器 (handler): {handler}")
    print(f"系统提示词 (system_prompt): {system_prompt}")

    # 准备测试数据
    test_data = [
        {"H": "AIRPLANE TOY (L码)"},
        {"H": "cotton t-shirt"},
        {"H": "T-SHIRT (XL) blue"},
        {"H": "polyster pants (M)"},
        {"H": "SHOES (Size 42)"}
    ]

    print("\n3. 输入数据")
    print("-" * 80)
    for i, item in enumerate(test_data, 1):
        print(f"{i}. {item['H']}")

    # 构建AI输入（从source_cols和depends_on获取数据）
    print("\n4. 构建AI输入")
    print("-" * 80)
    input_items = []
    for row_data in test_data:
        # 从source_cols获取数据
        for col in source_cols:
            value = row_data.get(col, '')
            input_items.append({"col": col, "value": value})

        # 从depends_on获取数据
        for col in depends_on:
            value = row_data.get(col, '')
            input_items.append({"col": col, "value": value})

    print(f"构建的输入项数量: {len(input_items)}")
    for i, item in enumerate(input_items[:5], 1):
        print(f"{i}. {item}")

    # 定义输出格式
    output_format = """要求：
1. 输入的数组顺序保持不变
2. 删除括号内冗余内容（如"AIRPLANE TOY (L码)"→"AIRPLANE TOY"）
3. 英文名称统一大写（"cotton t-shirt"→"COTTON T-SHIRT"）"""

    # 执行AI处理
    print("\n5. 执行AI处理")
    print("-" * 80)

    import time
    start_time = time.time()

    results = execute_ai_rule_batch(
        ai_service=ai_service,
        system_prompt=system_prompt,
        input_items=input_items,
        output_format=output_format
    )

    elapsed_time = time.time() - start_time
    print(f"处理完成！耗时：{elapsed_time:.2f}秒")

    # 显示结果
    print("\n6. 输出结果")
    print("-" * 80)
    for i, (input_item, result) in enumerate(zip(test_data, results), 1):
        original = input_item['H']
        cleaned = result if result else "[ERROR]"
        print(f"{i}. 输入: {original}")
        print(f"   输出: {cleaned}")
        print()

    # 验证结果
    print("=" * 80)
    print("验证结果")
    print("=" * 80)

    success_count = 0
    for i, (input_item, result) in enumerate(zip(test_data, results), 1):
        original = input_item['H']
        if result and result != '':
            is_upper = result.isupper()
            has_brackets = '(' in result or ')' in result

            status = "[OK]" if is_upper and not has_brackets else "[WARN]"
            print(f"{i}. {status}")
            print(f"   输入: {original}")
            print(f"   输出: {result}")
            print(f"   大写: {'是' if is_upper else '否'}")
            print(f"   无括号: {'是' if not has_brackets else '否'}")
            print()

            if is_upper and not has_brackets:
                success_count += 1

    print("=" * 80)
    print(f"总结: {success_count}/{len(test_data)} 条数据清理成功")
    print("=" * 80)

if __name__ == "__main__":
    test_h_column_from_db()
