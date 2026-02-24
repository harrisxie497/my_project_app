"""
检查DELIVERY类型的field_pipelines配置
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.core.database import SessionLocal
from app.models.field_pipeline import FieldPipeline

def check_delivery_field_pipelines_v2():
    """检查DELIVERY类型的field_pipelines配置"""
    print("=" * 100)
    print("检查DELIVERY类型的field_pipelines配置")
    print("=" * 100)
    
    db_session = SessionLocal()
    
    try:
        # 查询DELIVERY类型的field_pipelines
        field_pipelines = db_session.query(FieldPipeline).filter(
            FieldPipeline.file_type.like('%DELIVERY%')
        ).order_by(FieldPipeline.order_num).all()
        
        print(f"\nDELIVERY类型的field_pipelines（共{len(field_pipelines)}个）:")
        for idx, fp in enumerate(field_pipelines, start=1):
            print(f"\n  {idx}. 列名: {fp.target_col}")
            print(f"     表头: {fp.target_header}")
            print(f"     map_op: {fp.map_op}")
            print(f"     source_cols: {fp.source_cols}")
            print(f"     field_type: {fp.field_type}")
            print(f"     rule_ref: {fp.rule_ref}")
            print(f"     rule_params_json: {fp.rule_params_json}")
            print(f"     order_num: {fp.order_num}")
    
    except Exception as e:
        print(f"查询失败: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        db_session.close()
    
    print("\n" + "=" * 100)
    print("检查完成")
    print("=" * 100)

if __name__ == "__main__":
    check_delivery_field_pipelines_v2()
