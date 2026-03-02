"""
更新M列配置，添加add_prefix_zero参数
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.core.database import SessionLocal
from app.models.field_pipeline import FieldPipeline

def update_m_column():
    """更新M列配置，添加add_prefix_zero参数"""
    print("=" * 100)
    print("更新M列配置，添加add_prefix_zero参数")
    print("=" * 100)
    
    db_session = SessionLocal()
    
    try:
        # 查询CUSTOMS文件类型的M列配置
        m_column = db_session.query(FieldPipeline).filter(
            FieldPipeline.target_col == 'M',
            FieldPipeline.file_type == 'CUSTOMS'
        ).first()
        
        if m_column:
            print(f"\n当前配置：")
            print(f"  ID: {m_column.id}")
            print(f"  文件类型: {m_column.file_type}")
            print(f"  目标列: {m_column.target_col}")
            print(f"  规则参数: {m_column.rule_params_json}")
            print(f"  规则参数类型: {type(m_column.rule_params_json)}")
            
            # 修改 rule_params_json，添加 add_prefix_zero 参数
            import json
            
            # 如果 rule_params_json 是字符串，转换为字典
            if isinstance(m_column.rule_params_json, str):
                rule_params = json.loads(m_column.rule_params_json)
            else:
                rule_params = m_column.rule_params_json.copy()
            
            if 'policy_copy_regex' not in rule_params:
                rule_params['policy_copy_regex'] = {}
            
            rule_params['policy_copy_regex']['add_prefix_zero'] = True
            
            # 更新 rule_params_json
            m_column.rule_params_json = rule_params
            
            db_session.commit()
            
            print(f"\n✅ M列配置已更新")
            print(f"  新的规则参数: {m_column.rule_params_json}")
        else:
            print("\n❌ 未找到M列配置")
    
    finally:
        db_session.close()
    
    print("\n" + "=" * 100)
    print("更新完成")
    print("=" * 100)

if __name__ == "__main__":
    update_m_column()
