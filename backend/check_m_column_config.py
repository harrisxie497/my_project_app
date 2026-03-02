"""
查看M列的当前配置
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.core.database import SessionLocal
from app.models.field_pipeline import FieldPipeline

def check_m_column_config():
    """查看M列的当前配置"""
    print("=" * 100)
    print("查看M列（输入者电话番号）的当前配置")
    print("=" * 100)
    
    db_session = SessionLocal()
    
    try:
        # 查询M列的配置
        m_columns = db_session.query(FieldPipeline).filter(
            FieldPipeline.target_col == 'M'
        ).all()
        
        if not m_columns:
            print("\n❌ 未找到M列配置")
            return
        
        for idx, m_column in enumerate(m_columns, 1):
            print(f"\n{'=' * 100}")
            print(f"配置 {idx}")
            print(f"{'=' * 100}")
            print(f"  ID: {m_column.id}")
            print(f"  文件类型: {m_column.file_type}")
            print(f"  目标列: {m_column.target_col}")
            print(f"  目标表头: {m_column.target_header}")
            print(f"  操作类型: {m_column.map_op}")
            print(f"  源列: {m_column.source_cols}")
            print(f"  字段类型: {m_column.field_type}")
            print(f"  规则引用: {m_column.rule_ref}")
            print(f"  规则参数: {m_column.rule_params_json}")
            print(f"  依赖列: {m_column.depends_on}")
            print(f"  排序: {m_column.order_num}")
            print(f"  是否启用: {m_column.enabled}")
            print(f"  创建时间: {m_column.created_at}")
            print(f"  更新时间: {m_column.updated_at}")
    
    finally:
        db_session.close()
    
    print("\n" + "=" * 100)
    print("查看完成")
    print("=" * 100)

if __name__ == "__main__":
    check_m_column_config()
