"""
更新佐川顧客コード的固定值为"12345"
"""
from app.core.database import SessionLocal
from app.models.field_pipeline import FieldPipeline

db = SessionLocal()

try:
    # 查找N列的配置
    pipeline = db.query(FieldPipeline).filter(
        FieldPipeline.file_type == 'DELIVERY',
        FieldPipeline.target_col == 'N'
    ).first()
    
    if pipeline:
        # 更新为正确的固定值"12345"
        pipeline.rule_params_json = {
            "policy_const": {
                "value": "12345"
            }
        }
        db.commit()
        db.refresh(pipeline)
        
        print("[OK] 佐川顧客コード的固定值已更新为: 12345")
        print(f"  rule_params_json: {pipeline.rule_params_json}")
    else:
        print("[FAIL] 找不到N列的配置")
    
except Exception as e:
    print(f"错误: {str(e)}")
    db.rollback()
finally:
    db.close()
