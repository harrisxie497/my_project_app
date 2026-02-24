"""
检查A、B、C列的配置
"""
from app.core.database import SessionLocal
from app.models.field_pipeline import FieldPipeline

print("=" * 80)
print("检查A、B、C列的配置")
print("=" * 80)

db = SessionLocal()

try:
    target_columns = {
        'A': 'お客様管理番号',
        'B': '佐川問合せ番号HAWB',
        'C': '配達指定日'
    }

    for col, expected_header in target_columns.items():
        print(f"\n{'=' * 80}")
        print(f"列 {col} ({expected_header}):")
        print("-" * 80)

        pipeline = db.query(FieldPipeline).filter(
            FieldPipeline.file_type == 'DELIVERY',
            FieldPipeline.target_col == col,
            FieldPipeline.enabled == True
        ).first()

        if pipeline:
            print(f"  target_header: {pipeline.target_header}")
            print(f"  map_op: {pipeline.map_op}")
            print(f"  source_cols: {pipeline.source_cols}")
            print(f"  field_type: {pipeline.field_type}")
            print(f"  rule_ref: {pipeline.rule_ref}")
            print(f"  rule_params_json: {pipeline.rule_params_json}")
            print(f"  order_num: {pipeline.order_num}")
        else:
            print(f"  未找到配置")

    print("\n" + "=" * 80)

except Exception as e:
    print(f"错误: {str(e)}")
    import traceback
    traceback.print_exc()
finally:
    db.close()
