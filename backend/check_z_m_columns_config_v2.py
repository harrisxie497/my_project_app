"""
查询Z列和M列的电话号码配置
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.core.database import SessionLocal
from app.models.field_pipeline import FieldPipeline

def check_z_m_columns_config():
    """查询Z列和M列的电话号码配置"""
    print("=" * 100)
    print("查询Z列和M列的电话号码配置")
    print("=" * 100)
    
    db_session = SessionLocal()
    
    try:
        # 查询Z列的配置
        z_column = db_session.query(FieldPipeline).filter(
            FieldPipeline.target_col == 'Z',
            FieldPipeline.file_type == 'CUSTOMS'
        ).first()
        
        if z_column:
            print(f"\nZ列配置:")
            print(f"  ID: {z_column.id}")
            print(f"  目标列: {z_column.target_col}")
            print(f"  操作类型: {z_column.map_op}")
            print(f"  字段类型: {z_column.field_type}")
            print(f"  规则引用: {z_column.rule_ref}")
            print(f"  规则参数: {z_column.rule_params_json}")
        else:
            print("\n未找到Z列配置")
        
        # 查询M列的配置
        m_column = db_session.query(FieldPipeline).filter(
            FieldPipeline.target_col == 'M',
            FieldPipeline.file_type == 'CUSTOMS'
        ).first()
        
        if m_column:
            print(f"\nM列配置:")
            print(f"  ID: {m_column.id}")
            print(f"  目标列: {m_column.target_col}")
            print(f"  操作类型: {m_column.map_op}")
            print(f"  字段类型: {m_column.field_type}")
            print(f"  规则引用: {m_column.rule_ref}")
            print(f"  规则参数: {m_column.rule_params_json}")
        else:
            print("\n未找到M列配置")
    
    finally:
        db_session.close()
    
    print("\n" + "=" * 100)
    print("查询完成")
    print("=" * 100)

if __name__ == "__main__":
    check_z_m_columns_config()
