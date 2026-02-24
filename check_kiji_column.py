"""
查看記事欄2列的配置
"""
import sys
import os
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from app.core.database import SessionLocal
from app.models.field_pipeline import FieldPipeline

db = SessionLocal()

print("=" * 80)
print("查看記事欄2列的配置")
print("=" * 80)

# 查询記事欄2列
pipeline = db.query(FieldPipeline).filter(
    FieldPipeline.target_header == '記事欄2',
    FieldPipeline.file_type == 'DELIVERY'
).first()

if pipeline:
    print(f"\n当前配置:")
    print(f"  target_col: {pipeline.target_col}")
    print(f"  target_header: {pipeline.target_header}")
    print(f"  map_op: {pipeline.map_op}")
    print(f"  field_type: {pipeline.field_type}")
    print(f"  source_cols: {pipeline.source_cols}")
    print(f"  rule_ref: {pipeline.rule_ref}")
    print(f"  rule_params_json: {pipeline.rule_params_json}")
    print(f"  depends_on: {pipeline.depends_on}")
else:
    print("\n❌ 未找到記事欄2列的配置")

db.close()
