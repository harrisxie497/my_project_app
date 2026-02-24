"""
检查DELIVERY类型的SOURCE file_definitions配置
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.core.database import SessionLocal
from app.models.file_definition import FileDefinition

def check_delivery_source_file_definition():
    """检查DELIVERY类型的SOURCE file_definitions配置"""
    print("=" * 100)
    print("检查DELIVERY类型的SOURCE file_definitions配置")
    print("=" * 100)
    
    db_session = SessionLocal()
    
    try:
        # 查询DELIVERY类型的SOURCE file_definitions
        source_file_def = db_session.query(FileDefinition).filter(
            FileDefinition.file_type == 'DELIVERY',
            FileDefinition.file_role == 'SOURCE'
        ).first()
        
        if source_file_def:
            print(f"\nDELIVERY类型的SOURCE file_definitions:")
            print(f"  ID: {source_file_def.id}")
            print(f"  文件类型: {source_file_def.file_type}")
            print(f"  文件角色: {source_file_def.file_role}")
            print(f"  工作表名称: {source_file_def.sheet_name}")
            print(f"  表头行: {source_file_def.header_row}")
            print(f"  数据开始行: {source_file_def.data_start_row}")
            print(f"  列定义（共{len(source_file_def.columns_json)}列）:")
            for idx, col in enumerate(source_file_def.columns_json, start=1):
                print(f"    {idx}. {col['col']}: {col['header']}")
        else:
            print(f"\n未找到DELIVERY类型的SOURCE file_definitions")
    
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
    check_delivery_source_file_definition()
