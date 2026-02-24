"""
恢复記事欄2列的原始配置
"""
import sys
import os
import io
import json

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from app.core.database import SessionLocal
from sqlalchemy import text

db = SessionLocal()

print("=" * 80)
print("恢复記事欄2列的原始配置")
print("=" * 80)

try:
    # 恢复原始配置
    result = db.execute(text(
        "UPDATE field_pipelines "
        "SET map_op = 'CONST', "
        "    field_type = 'RULE_FIX', "
        "    source_cols = '[]', "
        "    rule_params_json = '{\"policy_const\": {\"value\": \"{{unique_code}}\"}}', "
        "    depends_on = '[]', "
        "    rule_ref = '[\"policy_const\"]' "
        "WHERE target_header = '記事欄2' AND file_type = 'DELIVERY'"
    ))

    db.commit()
    print("\n✅ 已恢复記事欄2列的原始配置")

    # 验证恢复
    verify_result = db.execute(text(
        "SELECT map_op, field_type, source_cols, rule_ref, rule_params_json "
        "FROM field_pipelines "
        "WHERE target_header = '記事欄2' AND file_type = 'DELIVERY'"
    )).fetchone()

    if verify_result:
        print(f"\n恢复后的配置:")
        print(f"  map_op: {verify_result[0]}")
        print(f"  field_type: {verify_result[1]}")
        print(f"  source_cols: {verify_result[2]}")
        print(f"  rule_ref: {verify_result[3]}")
        print(f"  rule_params_json: {verify_result[4]}")

except Exception as e:
    print(f"\n❌ 错误: {str(e)}")
    import traceback
    traceback.print_exc()
finally:
    db.close()
