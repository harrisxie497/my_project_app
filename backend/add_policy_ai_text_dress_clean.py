"""在rule_definitions表中添加policy_ai_text_dress_clean记录"""
import sys
import os
import json
from dotenv import load_dotenv

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine, text

def add_policy_ai_text_dress_clean():
    """添加policy_ai_text_dress_clean记录"""

    # 初始化数据库连接
    load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env'))
    database_url = os.getenv('DATABASE_URL')
    engine = create_engine(database_url)

    conn = engine.connect()

    # 1. 查询policy_ai_text_ja_clean作为参考
    print("1. 查询参考记录 policy_ai_text_ja_clean")
    print("-" * 80)

    result = conn.execute(text("""
        SELECT * FROM rule_definitions
        WHERE rule_ref = 'policy_ai_text_ja_clean'
    """))

    row = result.fetchone()
    if not row:
        print("未找到参考记录 policy_ai_text_ja_clean")
        conn.close()
        return

    columns = result.keys()
    ref_record = {col: row[i] for i, col in enumerate(columns)}

    schema_json = json.loads(ref_record['schema_json'])

    print(f"规则引用: {ref_record['rule_ref']}")
    print(f"规则类型: {ref_record['rule_type']}")
    print(f"执行器类型: {ref_record['executor_type']}")
    print(f"Schema描述: {schema_json.get('desc')}")
    print(f"处理器: {schema_json.get('handler')}")
    print(f"系统提示词: {schema_json.get('configurable_params', {}).get('system_prompt')[:100]}...")

    # 2. 创建新的记录
    print("\n2. 创建新记录 policy_ai_text_dress_clean")
    print("-" * 80)

    new_schema = {
        "desc": "收件人地址（日文）清洗：去括号备注，输出更清晰的地址格式（后台固定流程）",
        "handler": "ai.ja_address_clean",
        "configurable_params": {
            "system_prompt": "输入的数组数据是“收件人地址（日文）”，这是一个数组数组，针对每一个元素，去除括号内非地址部分（如“邮编备注”、“楼层备注”等），保留清晰的地址信息。只返回清理后的地址，每行一个，按顺序对应，不要包含其他文字。"
        }
    }

    insert_sql = """
        INSERT INTO rule_definitions (rule_ref, rule_type, executor_type, schema_json, enabled, created_at, updated_at)
        VALUES ('policy_ai_text_dress_clean', 'AI', 'ai', :schema_json, 1, NOW(), NULL)
    """

    try:
        result = conn.execute(text(insert_sql), {"schema_json": json.dumps(new_schema, ensure_ascii=False)})
        conn.commit()

        print("✓ 新记录已成功插入")
        print(f"\n新记录详情：")
        print(f"  规则引用: policy_ai_text_dress_clean")
        print(f"  规则类型: AI")
        print(f"  执行器类型: ai")
        print(f"  Schema描述: {new_schema.get('desc')}")
        print(f"  处理器: {new_schema.get('handler')}")
        print(f"  是否启用: 1")

    except Exception as e:
        conn.rollback()
        print(f"✗ 插入失败: {str(e)}")
        import traceback
        traceback.print_exc()

    # 3. 验证插入结果
    print("\n3. 验证插入结果")
    print("-" * 80)

    result = conn.execute(text("""
        SELECT rule_ref, rule_type, executor_type, enabled, created_at
        FROM rule_definitions
        WHERE rule_ref = 'policy_ai_text_dress_clean'
    """))

    row = result.fetchone()
    if row:
        print("✓ 记录已成功创建")
        print(f"  规则引用: {row[0]}")
        print(f"  规则类型: {row[1]}")
        print(f"  执行器类型: {row[2]}")
        print(f"  是否启用: {row[3]}")
        print(f"  创建时间: {row[4]}")
    else:
        print("✗ 记录未找到")

    conn.close()

    print("\n" + "=" * 80)
    print("操作完成")
    print("=" * 80)

if __name__ == "__main__":
    add_policy_ai_text_dress_clean()
