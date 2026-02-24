"""
查询file_definitions中OUTPUT的columns_json顺序
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.core.database import SessionLocal
from app.models.file_definition import FileDefinition
import json

def query_output_columns():
    """查询OUTPUT的columns_json"""
    print("=" * 100)
    print("查询file_definitions中OUTPUT的columns_json顺序")
    print("=" * 100)
    
    db_session = SessionLocal()
    
    try:
        # 查询OUTPUT文件定义
        output_file_def = db_session.query(FileDefinition).filter(
            FileDefinition.file_type == 'CUSTOMS',
            FileDefinition.file_role == 'OUTPUT'
        ).first()
        
        if output_file_def:
            print(f"\nOUTPUT文件定义:")
            print(f"  ID: {output_file_def.id}")
            print(f"  文件类型: {output_file_def.file_type}")
            print(f"  文件角色: {output_file_def.file_role}")
            print(f"  工作表名称: {output_file_def.sheet_name}")
            print(f"  表头行: {output_file_def.header_row}")
            print(f"  数据开始行: {output_file_def.data_start_row}")
            
            columns_json = output_file_def.columns_json
            print(f"\n列配置 (columns_json):")
            print(f"  列数: {len(columns_json)}")
            print(f"\n列顺序:")
            for idx, col in enumerate(columns_json, start=1):
                print(f"  {idx}. 列字母: {col.get('col')}, 表头: {col.get('header')}")
            
            print(f"\n表头列表:")
            headers = [col.get('header', '') for col in columns_json]
            print(f"  {headers}")
            
            print(f"\n完整JSON:")
            print(json.dumps(columns_json, ensure_ascii=False, indent=2))
        else:
            print("未找到OUTPUT文件定义")
    
    except Exception as e:
        print(f"查询失败: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        db_session.close()
    
    print("\n" + "=" * 100)
    print("查询完成")
    print("=" * 100)

if __name__ == "__main__":
    query_output_columns()
