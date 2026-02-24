"""
检查file_definitions的OUTPUT配置
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.core.database import SessionLocal
from app.models.file_definition import FileDefinition

def check_output_file_definition():
    """检查OUTPUT文件定义"""
    print("=" * 100)
    print("检查OUTPUT文件定义")
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
            
            print(f"\n列定义（共{len(output_file_def.columns_json)}列）:")
            for idx, col in enumerate(output_file_def.columns_json, start=1):
                print(f"  {idx}. {col['col']}: {col['header']}")
        else:
            print(f"\n未找到OUTPUT文件定义")
    
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
    check_output_file_definition()
