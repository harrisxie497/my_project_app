"""检查并更新policy_ai_text_dress_clean记录"""
import sys
import os
import json
from dotenv import load_dotenv

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine, text

def check_and_update_record():
    """检查并更新记录"""

    # 初始化数据库连接
    load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env'))
    database_url = os.getenv('DATABASE_URL')
    engine = create_engine(database_url)

    conn = engine.connect()

    # 1. 查询现有记录
    print("1. 查询现有记录")
    print("=" * 80)

    result = conn.execute(text("""
        SELECT * FROM rule_definitions
        WHERE rule_ref = 'policy_ai_text_dress_clean'
    """))

    row = result.fetchone()
    if row:
        columns = result.keys()
        record = {col: row[i] for i, col in enumerate(columns)}

        print("找到现有记录:")
        print(f"  规则引用: {record['rule_ref']}")
        print(f"  规则类型: {record['rule_type']}")
        print(f"  执行器类型: {record['executor_type']}")
        print(f"  是否启用: {record['enabled']}")

        schema_json = json.loads(record['schema_json'])
        print(f"  描述: {schema_json.get('desc')}")
        print(f"  处理器: {schema_json.get('handler')}")
        config_params = schema_json.get('configurable_params', {})
        print(f"  系统提示词: {config_params.get('system_prompt')[:100]}...")
    else:
        print("未找到记录，需要创建")

    # 2. 查询参考记录
    print("\n2. 查询参考记录 policy_ai_text_ja_clean")
    print("=" * 80)

    result = conn.execute(text("""
        SELECT * FROM rule_definitions
        WHERE rule_ref = 'policy_ai_text_ja_clean'
    """))

    row = result.fetchone()
    if row:
        columns = result.keys()
        ref_record = {col: row[i] for i, col in enumerate(columns)}

        schema_json = json.loads(ref_record['schema_json'])

        print(f"规则引用: {ref_record['rule_ref']}")
        print(f"  描述: {schema_json.get('desc')}")
        print(f"  处理器: {schema_json.get('handler')}")
        config_params = schema_json.get('configurable_params', {})
        print(f"  系统提示词: {config_params.get('system_prompt')[:100]}...")

        # 3. 创建新的schema（基于参考记录）
        print("\n3. 基于参考记录创建新schema")
        print("=" * 80)

        new_schema = {
            "desc": "收件人地址（日文）清洗：去括号备注，输出更清晰的地址格式（后台固定流程）",
            "handler": "ai.ja_address_clean",
            "configurable_params": {
                "system_prompt": "输入的数组数据是“收件人地址（日文）”，这是一个数组数组，针对每一个元素，去除括号内非地址部分（如“邮编备注”、“楼层备注”等），保留清晰的地址信息。只返回清理后的地址，每行一个，按顺序对应，不要包含其他文字。"
            }
        }

        print(f"新Schema描述: {new_schema.get('desc')}")
        print(f"新处理器: {new_schema.get('handler')}")

        # 4. 更新或插入记录
        print("\n4. 更新记录")
        print("=" * 80)

        try:
            # 尝试更新
            update_sql = """
                UPDATE rule_definitions
                SET schema_json = :schema_json,
                    updated_at = NOW()
                WHERE rule_ref = 'policy_ai_text_dress_clean'
            """

            result = conn.execute(text(update_sql), {"schema_json": json.dumps(new_schema, ensure_ascii=False)})
            conn.commit()

            print("[OK] 记录已成功更新")

        except Exception as e:
            conn.rollback()
            print(f"[ERROR] 更新失败: {str(e)}")

    conn.close()

    print("\n" + "=" * 80)
    print("操作完成")
    print("=" * 80)

if __name__ == "__main__":
    check_and_update_record()
