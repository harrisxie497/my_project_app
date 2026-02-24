"""
检查依頼主、依頼主住所、依頼主電話列的配置
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.core.database import SessionLocal
from app.models.field_pipeline import FieldPipeline

def check_default_columns_config():
    """检查DEFAULT类型列的配置"""
    print("=" * 100)
    print("检查依頼主、依頼主住所、依頼主電話列的配置")
    print("=" * 100)
    
    db_session = SessionLocal()
    
    try:
        # 查询这三列的field_pipelines配置
        columns_to_check = ['J', 'K', 'M']
        headers_to_check = ['依頼主', '依頼主住所', '依頼主電話']
        
        for col, header in zip(columns_to_check, headers_to_check):
            pipeline = db_session.query(FieldPipeline).filter(
                FieldPipeline.file_type.like('%DELIVERY%'),
                FieldPipeline.target_col == col
            ).first()
            
            if pipeline:
                print(f"\n{header}列（列{col}）的配置:")
                print(f"  列名: {pipeline.target_col}")
                print(f"  表头: {pipeline.target_header}")
                print(f"  map_op: {pipeline.map_op}")
                print(f"  source_cols: {pipeline.source_cols}")
                print(f"  field_type: {pipeline.field_type}")
                print(f"  rule_ref: {pipeline.rule_ref}")
                print(f"  rule_params_json: {pipeline.rule_params_json}")
                print(f"  depends_on: {pipeline.depends_on}")
                print(f"  order_num: {pipeline.order_num}")
            else:
                print(f"\n未找到{header}列（列{col}）的配置")
    
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
    check_default_columns_config()
