"""
检查輸入者電話番号和收件人电话列的配置
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.core.database import SessionLocal
from app.models.field_pipeline import FieldPipeline

def check_phone_columns_config():
    """检查輸入者電話番号和收件人电话列的配置"""
    print("=" * 100)
    print("检查輸入者電話番号和收件人电话列的配置")
    print("=" * 100)
    
    db_session = SessionLocal()
    
    try:
        # 查询輸入者電話番号列（CUSTOMS类型）
        customs_phone = db_session.query(FieldPipeline).filter(
            FieldPipeline.file_type == 'CUSTOMS',
            FieldPipeline.target_header.like('%輸入者電話番号%')
        ).first()
        
        if customs_phone:
            print(f"\n輸入者電話番号列（CUSTOMS类型）:")
            print(f"  列名: {customs_phone.target_col}")
            print(f"  表头: {customs_phone.target_header}")
            print(f"  map_op: {customs_phone.map_op}")
            print(f"  field_type: {customs_phone.field_type}")
            print(f"  rule_ref: {customs_phone.rule_ref}")
            print(f"  rule_params_json: {customs_phone.rule_params_json}")
        
        # 查询收件人电话列（CUSTOMS类型）
        customs_recipient_phone = db_session.query(FieldPipeline).filter(
            FieldPipeline.file_type == 'CUSTOMS',
            FieldPipeline.target_header.like('%收件人电话%')
        ).first()
        
        if customs_recipient_phone:
            print(f"\n收件人电话列（CUSTOMS类型）:")
            print(f"  列名: {customs_recipient_phone.target_col}")
            print(f"  表头: {customs_recipient_phone.target_header}")
            print(f"  map_op: {customs_recipient_phone.map_op}")
            print(f"  field_type: {customs_recipient_phone.field_type}")
            print(f"  rule_ref: {customs_recipient_phone.rule_ref}")
            print(f"  rule_params_json: {customs_recipient_phone.rule_params_json}")
        
        # 查询收件人电话列（DELIVERY类型）
        delivery_phone = db_session.query(FieldPipeline).filter(
            FieldPipeline.file_type == 'DELIVERY',
            FieldPipeline.target_header.like('%お届け先電話%')
        ).first()
        
        if delivery_phone:
            print(f"\n收件人电话列（DELIVERY类型）:")
            print(f"  列名: {delivery_phone.target_col}")
            print(f"  表头: {delivery_phone.target_header}")
            print(f"  map_op: {delivery_phone.map_op}")
            print(f"  field_type: {delivery_phone.field_type}")
            print(f"  rule_ref: {delivery_phone.rule_ref}")
            print(f"  rule_params_json: {delivery_phone.rule_params_json}")
    
    finally:
        db_session.close()
    
    print("\n" + "=" * 100)
    print("检查完成")
    print("=" * 100)

if __name__ == "__main__":
    check_phone_columns_config()
