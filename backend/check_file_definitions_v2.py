"""
检查为什么output_file_def会为None
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.core.database import SessionLocal
from app.models.file_definition import FileDefinition

def check_file_definitions():
    """检查file_definitions"""
    print("=" * 100)
    print("检查file_definitions")
    print("=" * 100)
    
    db_session = SessionLocal()
    
    try:
        # 查询所有文件定义
        file_definitions = db_session.query(FileDefinition).filter(
            FileDefinition.file_type == 'CUSTOMS'
        ).all()
        
        print(f"\n所有文件定义（共{len(file_definitions)}个）:")
        for fd in file_definitions:
            print(f"  文件类型: {fd.file_type}, 文件角色: {fd.file_role}, 工作表名称: {fd.sheet_name}")
        
        # 构建配置字典（与CustomsProcessor._load_file_definitions相同）
        configs = {}
        for fd in file_definitions:
            configs[fd.file_role] = {
                "id": fd.id,
                "file_type": fd.file_type,
                "file_role": fd.file_role,
                "sheet_name": fd.sheet_name,
                "header_row": fd.header_row,
                "data_start_row": fd.data_start_row,
                "columns_json": fd.columns_json
            }
        
        print(f"\n\n构建的配置字典:")
        print(f"  键: {list(configs.keys())}")
        print(f"  配置内容:")
        for key, value in configs.items():
            print(f"    {key}: {value}")
    
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
    check_file_definitions()
