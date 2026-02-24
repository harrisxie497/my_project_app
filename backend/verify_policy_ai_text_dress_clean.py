"""验证policy_ai_text_dress_clean记录"""
import sys
import os
import json
from dotenv import load_dotenv

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine, text

def verify_record():
    """验证记录"""

    # 初始化数据库连接
    load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env'))
    database_url = os.getenv('DATABASE_URL')
    engine = create_engine(database_url)

    conn = engine.connect()

    print("=" * 80)
    print("验证 policy_ai_text_dress_clean 记录")
    print("=" * 80)

    # 查询记录
    result = conn.execute(text("""
        SELECT * FROM rule_definitions
        WHERE rule_ref = 'policy_ai_text_dress_clean'
    """))

    row = result.fetchone()
    if row:
        columns = result.keys()
        record = {col: row[i] for i, col in enumerate(columns)}

        print("\n基本信息:")
        print(f"  规则引用: {record['rule_ref']}")
        print(f"  规则类型: {record['rule_type']}")
        print(f"  执行器类型: {record['executor_type']}")
        print(f"  是否启用: {record['enabled']}")
        print(f"  创建时间: {record['created_at']}")
        print(f"  更新时间: {record['updated_at']}")

        schema_json = json.loads(record['schema_json'])

        print("\nSchema配置:")
        print(f"  描述: {schema_json.get('desc')}")
        print(f"  处理器: {schema_json.get('handler')}")

        config_params = schema_json.get('configurable_params', {})
        system_prompt = config_params.get('system_prompt', '')

        print("\n系统提示词:")
        print(f"  {system_prompt}")

        print("\n完整JSON:")
        print(json.dumps(schema_json, indent=2, ensure_ascii=False))

        print("\n[OK] 记录验证成功")
    else:
        print("[ERROR] 未找到记录")

    # 对比参考记录
    print("\n" + "=" * 80)
    print("对比参考记录 policy_ai_text_ja_clean")
    print("=" * 80)

    result = conn.execute(text("""
        SELECT rule_ref, schema_json
        FROM rule_definitions
        WHERE rule_ref IN ('policy_ai_text_ja_clean', 'policy_ai_text_dress_clean')
        ORDER BY rule_ref
    """))

    print("\n规则对比:")
    print("-" * 80)
    for row in result:
        rule_ref = row[0]
        schema = json.loads(row[1])

        print(f"\n{rule_ref}:")
        print(f"  描述: {schema.get('desc')}")
        print(f"  处理器: {schema.get('handler')}")

    conn.close()

    print("\n" + "=" * 80)
    print("验证完成")
    print("=" * 80)

if __name__ == "__main__":
    verify_record()
