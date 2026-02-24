"""
检查依頼主、依頼主住所、依頼主電話三列的配置
"""
from app.core.database import SessionLocal
from app.models.field_pipeline import FieldPipeline
import json

print("=" * 80)
print("检查依頼主、依頼主住所、依頼主電話列的配置")
print("=" * 80)

db = SessionLocal()

try:
    # 获取J、K、M三列的配置
    target_columns = ['J', 'K', 'M']
    
    for col in target_columns:
        print(f"\n{'=' * 80}")
        print(f"列 {col}:")
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
