"""
检查电话号码的配置
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.core.database import SessionLocal
from app.models.field_pipeline import FieldPipeline

def check_phone_number_config():
    """检查电话号码的配置"""
    print("=" * 100)
    print("检查电话号码的配置")
    print("=" * 100)
    
    db_session = SessionLocal()
    
    try:
        # 查询电话号码相关的field_pipelines
        phone_pipelines = db_session.query(FieldPipeline).filter(
            FieldPipeline.file_type.like('%CUSTOMS%'),
            FieldPipeline.target_header.in_(['輸入者電話番号', '收件人电话'])
        ).order_by(FieldPipeline.order_num).all()
        
        print(f"\n电话号码相关的field_pipelines（共{len(phone_pipelines)}个）:")
        for fp in phone_pipelines:
            print(f"\n  列名: {fp.target_col}")
            print(f"  表头: {fp.target_header}")
            print(f"  map_op: {fp.map_op}")
            print(f"  source_cols: {fp.source_cols}")
            print(f"  field_type: {fp.field_type}")
            print(f"  rule_ref: {fp.rule_ref}")
            print(f"  rule_params_json: {fp.rule_params_json}")
            print(f"  order_num: {fp.order_num}")
    
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
    check_phone_number_config()
