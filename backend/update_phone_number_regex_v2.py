"""
更新电话号码的正则表达式（直接更新数据库）
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.core.database import SessionLocal
from app.models.field_pipeline import FieldPipeline
import json

def update_phone_number_regex():
    """更新电话号码的正则表达式"""
    print("=" * 100)
    print("更新电话号码的正则表达式")
    print("=" * 100)
    
    db_session = SessionLocal()
    
    try:
        # 查询电话号码相关的field_pipelines
        phone_pipelines = db_session.query(FieldPipeline).filter(
            FieldPipeline.file_type.like('%CUSTOMS%'),
            FieldPipeline.target_header.in_(['輸入者電話番号', '收件人电话'])
        ).all()
        
        print(f"\n更新前的电话号码配置（共{len(phone_pipelines)}个）:")
        for fp in phone_pipelines:
            print(f"  列名: {fp.target_col}, 表头: {fp.target_header}")
            print(f"  rule_params_json: {fp.rule_params_json}")
            
            # 更新正则表达式
            if fp.rule_params_json and 'policy_copy_regex' in fp.rule_params_json:
                # 创建新的rule_params_json
                new_rule_params_json = fp.rule_params_json.copy()
                new_rule_params_json['policy_copy_regex']['regex'] = r'^0\d{9,11}$'
                
                # 更新数据库
                fp.rule_params_json = new_rule_params_json
                db_session.commit()
                print(f"  ✓ 更新正则表达式为: {new_rule_params_json['policy_copy_regex']['regex']}")
        
        print(f"\n✓ 更新成功！")
    
    except Exception as e:
        print(f"更新失败: {e}")
        import traceback
        traceback.print_exc()
        db_session.rollback()
    
    finally:
        db_session.close()
    
    print("\n" + "=" * 100)
    print("更新完成")
    print("=" * 100)

if __name__ == "__main__":
    update_phone_number_regex()
