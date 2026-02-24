"""
检查D列的当前配置
"""
from app.core.database import SessionLocal
from app.models.field_pipeline import FieldPipeline

print("=" * 80)
print("检查D列（時間帯指定）的配置")
print("=" * 80)

db = SessionLocal()

try:
    pipeline = db.query(FieldPipeline).filter(
        FieldPipeline.file_type == 'DELIVERY',
        FieldPipeline.target_col == 'D',
        FieldPipeline.enabled == True
    ).first()

    if pipeline:
        print(f"\n当前配置:")
        print(f"  target_col: {pipeline.target_col}")
        print(f"  target_header: {pipeline.target_header}")
        print(f"  map_op: {pipeline.map_op}")
        print(f"  source_cols: {pipeline.source_cols}")
        print(f"  field_type: {pipeline.field_type}")
        print(f"  rule_ref: {pipeline.rule_ref}")
        print(f"  rule_params_json: {pipeline.rule_params_json}")
        print(f"  depends_on: {pipeline.depends_on}")
        print(f"  order_num: {pipeline.order_num}")
    else:
        print(f"\n未找到D列的配置")

    print("\n" + "=" * 80)

except Exception as e:
    print(f"错误: {str(e)}")
    import traceback
    traceback.print_exc()
finally:
    db.close()
