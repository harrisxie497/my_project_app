"""
检查收件地址列的配置
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.core.database import SessionLocal
from app.models.field_pipeline import FieldPipeline

def check_address_column_config():
    """检查收件地址列的配置"""
    print("=" * 100)
    print("检查收件地址列的配置")
    print("=" * 100)
    
    db_session = SessionLocal()
    
    try:
        # 查询收件地址列（CUSTOMS类型）
        customs_address = db_session.query(FieldPipeline).filter(
            FieldPipeline.file_type == 'CUSTOMS',
            FieldPipeline.target_header.like('%收件人地址%')
        ).first()
        
        if customs_address:
            print(f"\n收件人地址列（CUSTOMS类型）:")
            print(f"  列名: {customs_address.target_col}")
            print(f"  表头: {customs_address.target_header}")
            print(f"  map_op: {customs_address.map_op}")
            print(f"  field_type: {customs_address.field_type}")
            print(f"  rule_ref: {customs_address.rule_ref}")
            print(f"  source_cols: {customs_address.source_cols}")
            print(f"  depends_on: {customs_address.depends_on}")
            print(f"  rule_params_json: {customs_address.rule_params_json}")
        
        # 查询收件地址列（DELIVERY类型）
        delivery_address = db_session.query(FieldPipeline).filter(
            FieldPipeline.file_type == 'DELIVERY',
            FieldPipeline.target_header.like('%お届け先住所%')
        ).first()
        
        if delivery_address:
            print(f"\n收件地址列（DELIVERY类型）:")
            print(f"  列名: {delivery_address.target_col}")
            print(f"  表头: {delivery_address.target_header}")
            print(f"  map_op: {delivery_address.map_op}")
            print(f"  field_type: {delivery_address.field_type}")
            print(f"  rule_ref: {delivery_address.rule_ref}")
            print(f"  source_cols: {delivery_address.source_cols}")
            print(f"  depends_on: {delivery_address.depends_on}")
            print(f"  rule_params_json: {delivery_address.rule_params_json}")
    
    finally:
        db_session.close()
    
    print("\n" + "=" * 100)
    print("检查完成")
    print("=" * 100)

if __name__ == "__main__":
    check_address_column_config()
