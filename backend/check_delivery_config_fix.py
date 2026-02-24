"""
检查DELIVERY配置，特别是CONST操作的配置
"""
from app.core.database import SessionLocal
from app.models.field_pipeline import FieldPipeline
import json

print("=" * 80)
print("检查DELIVERY的FieldPipeline配置（重点关注CONST操作）")
print("=" * 80)

db = SessionLocal()

try:
    pipelines = db.query(FieldPipeline).filter(
        FieldPipeline.file_type == 'DELIVERY',
        FieldPipeline.map_op == 'CONST'
    ).all()
    
    print(f"\n找到 {len(pipelines)} 个CONST操作:")
    print("-" * 80)
    
    for p in pipelines:
        print(f"\n列 {p.target_col}: {p.target_header}")
        print(f"  map_op: {p.map_op}")
        print(f"  source_cols: {p.source_cols}")
        print(f"  field_type: {p.field_type}")
        print(f"  rule_ref: {p.rule_ref}")
        print(f"  rule_params_json: {p.rule_params_json}")
        print(f"  depends_on: {p.depends_on}")
        print(f"  order_num: {p.order_num}")
        print(f"  enabled: {p.enabled}")
        
        if p.rule_params_json:
            print(f"\n  详细配置:")
            if isinstance(p.rule_params_json, str):
                print(f"    (JSON字符串): {p.rule_params_json}")
                try:
                    params = json.loads(p.rule_params_json)
                    print(f"    (解析后): {json.dumps(params, indent=4, ensure_ascii=False)}")
                except Exception as e:
                    print(f"    解析失败: {e}")
            else:
                print(f"    (对象): {json.dumps(p.rule_params_json, indent=4, ensure_ascii=False)}")
    
    print("\n" + "=" * 80)
    
except Exception as e:
    print(f"错误: {str(e)}")
    import traceback
    traceback.print_exc()
finally:
    db.close()
