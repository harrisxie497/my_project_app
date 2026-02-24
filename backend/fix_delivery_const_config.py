"""
修复DELIVERY配置中的CONST操作
为N列添加正确的rule_params_json
"""
from app.core.database import SessionLocal
from app.models.field_pipeline import FieldPipeline
import json

print("=" * 80)
print("修复DELIVERY的CONST操作配置")
print("=" * 80)

db = SessionLocal()

try:
    # 查找N列的配置
    pipeline = db.query(FieldPipeline).filter(
        FieldPipeline.file_type == 'DELIVERY',
        FieldPipeline.target_col == 'N'
    ).first()
    
    if not pipeline:
        print("[FAIL] 找不到N列的配置")
    else:
        print(f"\n当前配置:")
        print(f"  列: {pipeline.target_col}")
        print(f"  表头: {pipeline.target_header}")
        print(f"  map_op: {pipeline.map_op}")
        print(f"  rule_params_json: {pipeline.rule_params_json}")
        
        # 更新配置 - 添加正确的rule_params_json
        # 根据佐川急便的业务需求，佐川顧客コード应该是一个固定值
        # 这里我们暂时使用一个示例值，实际值需要根据业务需求确定
        new_rule_params = {
            "policy_const": {
                "value": "123456"  # 示例值，需要根据实际业务需求修改
            }
        }
        
        print(f"\n新配置:")
        print(f"  rule_params_json: {json.dumps(new_rule_params, ensure_ascii=False, indent=2)}")
        
        # 更新数据库
        pipeline.rule_params_json = new_rule_params
        db.commit()
        db.refresh(pipeline)
        
        print(f"\n[OK] 配置已更新")
        print(f"  更新后的rule_params_json: {pipeline.rule_params_json}")
    
    print("\n" + "=" * 80)
    print("[注意] 请根据实际业务需求修改佐川顧客コード的固定值")
    print("当前使用的值是: 123456")
    print("如需修改，请更新field_pipelines表中N列的rule_params_json")
    print("=" * 80)
    
except Exception as e:
    print(f"错误: {str(e)}")
    import traceback
    traceback.print_exc()
    db.rollback()
finally:
    db.close()
