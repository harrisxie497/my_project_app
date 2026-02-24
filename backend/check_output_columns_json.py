"""
检查为什么file_definitions的OUTPUT的columns_json顺序没有被正确使用
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.core.database import SessionLocal
from app.models.file_definition import FileDefinition

def check_output_columns_json():
    """检查OUTPUT的columns_json"""
    print("=" * 100)
    print("检查OUTPUT的columns_json")
    print("=" * 100)
    
    db_session = SessionLocal()
    
    try:
        # 查询OUTPUT文件定义
        output_file_def = db_session.query(FileDefinition).filter(
            FileDefinition.file_type == 'CUSTOMS',
            FileDefinition.file_role == 'OUTPUT'
        ).first()
        
        if output_file_def:
            columns_json = output_file_def.columns_json
            print(f"\nOUTPUT的columns_json:")
            print(f"  类型: {type(columns_json)}")
            print(f"  长度: {len(columns_json)}")
            print(f"\n列顺序:")
            for idx, col in enumerate(columns_json, start=1):
                print(f"  {idx}. 列字母: {col.get('col')}, 表头: {col.get('header')}")
        else:
            print("未找到OUTPUT文件定义")
    
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
    check_output_columns_json()
