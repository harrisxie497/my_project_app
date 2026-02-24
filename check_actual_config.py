"""
查询数据库中記事欄2和D列的实际配置
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
print("查询数据库中的实际配置")
print("=" * 80)

# 查询記事欄2列
print("\n記事欄2列的配置:")
pipeline_kiji = db.query(FieldPipeline).filter(
    FieldPipeline.target_header == '記事欄2',
    FieldPipeline.file_type == 'DELIVERY'
).first()

if pipeline_kiji:
    print(f"  target_col: {pipeline_kiji.target_col}")
    print(f"  target_header: {pipeline_kiji.target_header}")
    print(f"  map_op: {pipeline_kiji.map_op}")
    print(f"  source_cols: {pipeline_kiji.source_cols}")
    print(f"  field_type: {pipeline_kiji.field_type}")
    print(f"  rule_ref: {pipeline_kiji.rule_ref}")
    print(f"  rule_params_json: {pipeline_kiji.rule_params_json}")

# 查询D列
print("\nD列（時間帯指定）的配置:")
pipeline_d = db.query(FieldPipeline).filter(
    FieldPipeline.target_col == 'D',
    FieldPipeline.file_type == 'DELIVERY'
).first()

if pipeline_d:
    print(f"  target_col: {pipeline_d.target_col}")
    print(f"  target_header: {pipeline_d.target_header}")
    print(f"  map_op: {pipeline_d.map_op}")
    print(f"  source_cols: {pipeline_d.source_cols}")
    print(f"  field_type: {pipeline_d.field_type}")
    print(f"  rule_ref: {pipeline_d.rule_ref}")
    print(f"  depends_on: {pipeline_d.depends_on}")
    print(f"  rule_params_json: {pipeline_d.rule_params_json}")

db.close()
