"""
回退記事欄2列的配置到之前的方式
"""
import sys
import os
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from app.core.database import SessionLocal
from sqlalchemy import text

db = SessionLocal()

print("=" * 80)
print("回退記事欄2列的配置")
print("=" * 80)

try:
    # 回退到之前的配置
    result = db.execute(text(
        "UPDATE field_pipelines "
        "SET map_op = 'COPY', "
        "    field_type = 'TEXT', "
        "    source_cols = '[\"記事欄2\"]', "
        "    rule_params_json = NULL, "
        "    depends_on = '[]' "
        "WHERE target_header = '記事欄2' AND file_type = 'DELIVERY'"
    ))

    db.commit()
    print("\n✅ 已回退記事欄2列的配置到之前的COPY方式")

    # 验证回退
    verify_result = db.execute(text(
        "SELECT map_op, field_type, source_cols, rule_params_json "
        "FROM field_pipelines "
        "WHERE target_header = '記事欄2' AND file_type = 'DELIVERY'"
    )).fetchone()

    if verify_result:
        print(f"\n回退后的配置:")
        print(f"  map_op: {verify_result[0]}")
        print(f"  field_type: {verify_result[1]}")
        print(f"  source_cols: {verify_result[2]}")
        print(f"  rule_params_json: {verify_result[3]}")

except Exception as e:
    print(f"\n❌ 错误: {str(e)}")
    import traceback
    traceback.print_exc()
finally:
    db.close()
