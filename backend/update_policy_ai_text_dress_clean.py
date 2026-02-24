"""更新policy_ai_text_dress_clean的配置"""
import sys
import os
import json
from dotenv import load_dotenv

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine, text

def update_record():
    """更新记录配置"""

    # 初始化数据库连接
    load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env'))
    database_url = os.getenv('DATABASE_URL')
    engine = create_engine(database_url)

    conn = engine.connect()

    # 1. 查询现有记录
    print("1. 查询现有记录")
    print("-" * 80)

    result = conn.execute(text("""
        SELECT * FROM rule_definitions
        WHERE rule_ref = 'policy_ai_text_dress_clean'
    """))

    row = result.fetchone()
    if not row:
        print("未找到记录")
        conn.close()
        return

    columns = result.keys()
    record = {col: row[i] for i, col in enumerate(columns)}
    old_schema = json.loads(record['schema_json'])

    print(f"当前配置:")
    print(f"  handler: {old_schema.get('handler')}")
    print(f"  系统提示词: {old_schema.get('configurable_params', {}).get('system_prompt', '')[:100]}...")

    # 2. 更新schema
    print("\n2. 更新Schema配置")
    print("-" * 80)

    new_system_prompt = """如果输入的数组数据是"收件人地址"，这是一个数组数组，针对每一个元素，将日本地址名精准翻译成英文，确保语义准确无误，由于是日本地址，请翻译成罗马大写，顺序按照顺序为"都道府县 → 市/区 → 町/地区 → 丁目/番地" 方式；例如："AICHI KEN  NAGOYA SHI NAKAGAWA KU  KAMINAGARECHO 1-10-101" 中间不需要加标点符号，可以加入空格；但是在门牌的部分不能有空格。（例如：1-10-101这种就很好，在-两边都不需要有空格）翻译结果需全部大写（包括字母、数字、特殊符号内的字符，仅保持原始标点符号）。对于输出的要求，也是一个数组，并且顺序和数组长度保持输入的一样。"""

    new_schema = {
        "desc": "收件人地址（日文）翻译：翻译为英文（罗马大写），保持标准地址格式（后台固定流程）",
        "handler": "ai.ja_address_clean",
        "configurable_params": {
            "system_prompt": new_system_prompt
        }
    }

    print(f"新handler: {new_schema.get('handler')}")
    print(f"新系统提示词: {new_schema.get('configurable_params', {}).get('system_prompt')[:100]}...")

    # 3. 执行更新
    print("\n3. 执行更新")
    print("-" * 80)

    update_sql = """
        UPDATE rule_definitions
        SET schema_json = :schema_json,
            updated_at = NOW()
        WHERE rule_ref = 'policy_ai_text_dress_clean'
    """

    try:
        result = conn.execute(text(update_sql), {"schema_json": json.dumps(new_schema, ensure_ascii=False)})
        conn.commit()

        print("[OK] 记录已成功更新")

    except Exception as e:
        conn.rollback()
        print(f"[ERROR] 更新失败: {str(e)}")
        import traceback
        traceback.print_exc()

    # 4. 验证更新结果
    print("\n4. 验证更新结果")
    print("-" * 80)

    result = conn.execute(text("""
        SELECT rule_ref, schema_json, updated_at
        FROM rule_definitions
        WHERE rule_ref = 'policy_ai_text_dress_clean'
    """))

    row = result.fetchone()
    if row:
        schema = json.loads(row[1])
        print("[OK] 记录已成功更新")
        print(f"  规则引用: {row[0]}")
        print(f"  更新时间: {row[2]}")
        print(f"  Handler: {schema.get('handler')}")
        print(f"  描述: {schema.get('desc')}")

        system_prompt = schema.get('configurable_params', {}).get('system_prompt', '')
        print(f"  系统提示词长度: {len(system_prompt)} 字符")

    conn.close()

    print("\n" + "=" * 80)
    print("更新完成")
    print("=" * 80)

if __name__ == "__main__":
    update_record()
