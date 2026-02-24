"""
检查D列的depends_on配置
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.core.database import SessionLocal
from app.models.field_pipeline import FieldPipeline

def check_d_column_depends_on():
    """检查D列的depends_on配置"""
    print("=" * 100)
    print("检查D列的depends_on配置")
    print("=" * 100)
    
    db_session = SessionLocal()
    
    try:
        # 查询D列的field_pipelines配置
        d_pipeline = db_session.query(FieldPipeline).filter(
            FieldPipeline.file_type.like('%DELIVERY%'),
            FieldPipeline.target_col == 'D'
        ).first()
        
        if d_pipeline:
            print(f"\nD列的field_pipelines配置:")
            print(f"  列名: {d_pipeline.target_col}")
            print(f"  表头: {d_pipeline.target_header}")
            print(f"  map_op: {d_pipeline.map_op}")
            print(f"  source_cols: {d_pipeline.source_cols}")
            print(f"  field_type: {d_pipeline.field_type}")
            print(f"  rule_ref: {d_pipeline.rule_ref}")
            print(f"  rule_params_json: {d_pipeline.rule_params_json}")
            print(f"  depends_on: {d_pipeline.depends_on}")
            print(f"  order_num: {d_pipeline.order_num}")
        else:
            print(f"\n未找到D列的field_pipelines配置")
    
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
    check_d_column_depends_on()
