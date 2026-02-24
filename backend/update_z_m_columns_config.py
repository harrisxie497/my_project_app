"""
修改Z列和M列的电话号码配置
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.core.database import SessionLocal
from app.models.field_pipeline import FieldPipeline
import json

def update_phone_columns_config():
    """修改Z列和M列的电话号码配置"""
    print("=" * 100)
    print("修改Z列和M列的电话号码配置")
    print("=" * 100)
    
    db_session = SessionLocal()
    
    try:
        # 修改Z列的配置
        z_column = db_session.query(FieldPipeline).filter(
            FieldPipeline.target_col == 'Z',
            FieldPipeline.file_type == 'CUSTOMS'
        ).first()
        
        if z_column:
            print(f"\n修改Z列配置:")
            print(f"  原配置: {z_column.rule_params_json}")
            
            # 更新规则参数
            new_rule_params = {
                'policy_copy_regex': {
                    'regex': '^\\d{9,11}$',
                    'required': True,
                    'remove_dash': True
                }
            }
            
            z_column.rule_params_json = json.dumps(new_rule_params)
            db_session.commit()
            
            print(f"  新配置: {z_column.rule_params_json}")
            print(f"  Z列配置修改成功")
        else:
            print("\n未找到Z列配置")
        
        # 修改M列的配置
        m_column = db_session.query(FieldPipeline).filter(
            FieldPipeline.target_col == 'M',
            FieldPipeline.file_type == 'CUSTOMS'
        ).first()
        
        if m_column:
            print(f"\n修改M列配置:")
            print(f"  原配置: {m_column.rule_params_json}")
            
            # 更新规则参数
            new_rule_params = {
                'policy_copy_regex': {
                    'regex': '^\\d{9,11}$',
                    'required': True,
                    'remove_dash': True
                }
            }
            
            m_column.rule_params_json = json.dumps(new_rule_params)
            db_session.commit()
            
            print(f"  新配置: {m_column.rule_params_json}")
            print(f"  M列配置修改成功")
        else:
            print("\n未找到M列配置")
    
    except Exception as e:
        print(f"\n修改失败: {e}")
        import traceback
        traceback.print_exc()
        db_session.rollback()
    finally:
        db_session.close()
    
    print("\n" + "=" * 100)
    print("修改完成")
    print("=" * 100)

if __name__ == "__main__":
    update_phone_columns_config()
