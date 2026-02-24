"""
检查記事欄2列的处理逻辑
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.core.database import SessionLocal
from app.models.field_pipeline import FieldPipeline

def check_p_column_config():
    """检查記事欄2列的配置"""
    print("=" * 100)
    print("检查記事欄2列的配置")
    print("=" * 100)
    
    db_session = SessionLocal()
    
    try:
        # 查询記事欄2列的field_pipelines配置
        p_pipeline = db_session.query(FieldPipeline).filter(
            FieldPipeline.file_type.like('%DELIVERY%'),
            FieldPipeline.target_col == 'P'
        ).first()
        
        if p_pipeline:
            print(f"\n記事欄2列的field_pipelines配置:")
            print(f"  列名: {p_pipeline.target_col}")
            print(f"  表头: {p_pipeline.target_header}")
            print(f"  map_op: {p_pipeline.map_op}")
            print(f"  source_cols: {p_pipeline.source_cols}")
            print(f"  field_type: {p_pipeline.field_type}")
            print(f"  rule_ref: {p_pipeline.rule_ref}")
            print(f"  rule_params_json: {p_pipeline.rule_params_json}")
            print(f"  depends_on: {p_pipeline.depends_on}")
            print(f"  order_num: {p_pipeline.order_num}")
        else:
            print(f"\n未找到記事欄2列的field_pipelines配置")
    
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
    check_p_column_config()
