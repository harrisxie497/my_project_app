"""
更新Z列和M列的配置，添加去除前后空格和去除中间空格的参数
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.core.database import SessionLocal
from app.models.field_pipeline import FieldPipeline
import json

def update_z_m_columns_config():
    """更新Z列和M列的配置"""
    print("=" * 100)
    print("更新Z列和M列的配置")
    print("=" * 100)
    
    db_session = SessionLocal()
    
    try:
        # 更新Z列的配置
        z_column = db_session.query(FieldPipeline).filter(
            FieldPipeline.target_col == 'Z',
            FieldPipeline.file_type == 'CUSTOMS'
        ).first()
        
        if z_column:
            print(f"\n更新前Z列配置:")
            print(f"  规则参数: {z_column.rule_params_json}")
            
            # 解析现有的rule_params_json
            rule_params = json.loads(z_column.rule_params_json) if isinstance(z_column.rule_params_json, str) else z_column.rule_params_json
            
            # 添加去除前后空格和去除中间空格的参数
            rule_params['policy_copy_regex']['remove_leading_trailing_spaces'] = True
            rule_params['policy_copy_regex']['remove_middle_spaces'] = True
            
            # 更新配置
            z_column.rule_params_json = json.dumps(rule_params, ensure_ascii=False)
            
            print(f"\n更新后Z列配置:")
            print(f"  规则参数: {z_column.rule_params_json}")
            
            db_session.commit()
            print(f"\nZ列配置更新成功")
        else:
            print("\n未找到Z列配置")
        
        # 更新M列的配置
        m_column = db_session.query(FieldPipeline).filter(
            FieldPipeline.target_col == 'M',
            FieldPipeline.file_type == 'CUSTOMS'
        ).first()
        
        if m_column:
            print(f"\n更新前M列配置:")
            print(f"  规则参数: {m_column.rule_params_json}")
            
            # 解析现有的rule_params_json
            rule_params = json.loads(m_column.rule_params_json) if isinstance(m_column.rule_params_json, str) else m_column.rule_params_json
            
            # 添加去除前后空格和去除中间空格的参数
            rule_params['policy_copy_regex']['remove_leading_trailing_spaces'] = True
            rule_params['policy_copy_regex']['remove_middle_spaces'] = True
            
            # 更新配置
            m_column.rule_params_json = json.dumps(rule_params, ensure_ascii=False)
            
            print(f"\n更新后M列配置:")
            print(f"  规则参数: {m_column.rule_params_json}")
            
            db_session.commit()
            print(f"\nM列配置更新成功")
        else:
            print("\n未找到M列配置")
    
    finally:
        db_session.close()
    
    print("\n" + "=" * 100)
    print("更新完成")
    print("=" * 100)

if __name__ == "__main__":
    update_z_m_columns_config()
