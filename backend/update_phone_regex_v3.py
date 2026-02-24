"""
更新輸入者電話番号和收件人电话列的regex配置
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.core.database import SessionLocal
from app.models.field_pipeline import FieldPipeline

def update_phone_regex():
    """更新輸入者電話番号和收件人电话列的regex配置"""
    print("=" * 100)
    print("更新輸入者電話番号和收件人电话列的regex配置")
    print("=" * 100)
    
    db_session = SessionLocal()
    
    try:
        # 查询并更新輸入者電話番号列（CUSTOMS类型）
        customs_phone = db_session.query(FieldPipeline).filter(
            FieldPipeline.file_type == 'CUSTOMS',
            FieldPipeline.target_header.like('%輸入者電話番号%')
        ).first()
        
        if customs_phone and customs_phone.rule_params_json:
            print(f"\n更新前 - 輸入者電話番号列:")
            print(f"  rule_params_json: {customs_phone.rule_params_json}")
            
            # 更新regex
            customs_phone.rule_params_json['policy_copy_regex']['regex'] = r'^\d{9,11}$'
            
            print(f"\n更新后 - 輸入者電話番号列:")
            print(f"  rule_params_json: {customs_phone.rule_params_json}")
        
        # 查询并更新收件人电话列（CUSTOMS类型）
        customs_recipient_phone = db_session.query(FieldPipeline).filter(
            FieldPipeline.file_type == 'CUSTOMS',
            FieldPipeline.target_header.like('%收件人电话%')
        ).first()
        
        if customs_recipient_phone and customs_recipient_phone.rule_params_json:
            print(f"\n更新前 - 收件人电话列（CUSTOMS类型）:")
            print(f"  rule_params_json: {customs_recipient_phone.rule_params_json}")
            
            # 更新regex
            customs_recipient_phone.rule_params_json['policy_copy_regex']['regex'] = r'^\d{9,11}$'
            
            print(f"\n更新后 - 收件人电话列（CUSTOMS类型）:")
            print(f"  rule_params_json: {customs_recipient_phone.rule_params_json}")
        
        # 查询并更新收件人电话列（DELIVERY类型）
        delivery_phone = db_session.query(FieldPipeline).filter(
            FieldPipeline.file_type == 'DELIVERY',
            FieldPipeline.target_header.like('%お届け先電話%')
        ).first()
        
        if delivery_phone and delivery_phone.rule_params_json:
            print(f"\n更新前 - 收件人电话列（DELIVERY类型）:")
            print(f"  rule_params_json: {delivery_phone.rule_params_json}")
            
            # 更新regex
            delivery_phone.rule_params_json['policy_copy_regex']['regex'] = r'^\d{9,11}$'
            
            print(f"\n更新后 - 收件人电话列（DELIVERY类型）:")
            print(f"  rule_params_json: {delivery_phone.rule_params_json}")
        
        # 提交更改
        db_session.commit()
        print("\n" + "=" * 100)
        print("数据库更新成功")
        print("=" * 100)
    
    except Exception as e:
        db_session.rollback()
        print(f"\n更新失败: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db_session.close()

if __name__ == "__main__":
    update_phone_regex()
