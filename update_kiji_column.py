"""
修改記事欄2列的配置，使用task_id
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
print("修改記事欄2列的配置")
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

    # 修改为DEFAULT操作，使用task_id
    pipeline.map_op = 'DEFAULT'
    pipeline.field_type = 'HEADER'
    pipeline.rule_params_json = 'task_id'  # 使用header_params中的task_id
    pipeline.source_cols = []  # 清空source_cols

    db.commit()

    print(f"\n✅ 已修改配置:")
    print(f"  map_op: DEFAULT")
    print(f"  field_type: HEADER")
    print(f"  rule_params_json: 'task_id'")
    print(f"  说明: 記事欄2将使用header_params中的task_id值")

    # 验证修改
    db.refresh(pipeline)
    print(f"\n修改后的配置:")
    print(f"  map_op: {pipeline.map_op}")
    print(f"  field_type: {pipeline.field_type}")
    print(f"  rule_params_json: {pipeline.rule_params_json}")
else:
    print("\n❌ 未找到記事欄2列的配置")

db.close()
