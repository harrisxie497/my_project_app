"""
检查_generate_result_file方法中的file_definitions
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.core.database import SessionLocal
from app.services.customs_processor import CustomsProcessor

def check_generate_result_file():
    """检查_generate_result_file方法中的file_definitions"""
    print("=" * 100)
    print("检查_generate_result_file方法中的file_definitions")
    print("=" * 100)
    
    db_session = SessionLocal()
    
    try:
        # 创建CustomsProcessor实例
        task_dir = r'C:\Users\harris.xie\Documents\trae_projects\japan\backend\storage\tasks\t_aa9d170a'
        processor = CustomsProcessor(db_session=db_session, task_dir=task_dir, file_type='CUSTOMS')
        
        print(f"\nCustomsProcessor初始化完成:")
        print(f"  file_type: {processor.file_type}")
        print(f"  file_definitions: {processor.file_definitions}")
        
        # 加载file_definitions
        file_definitions = processor._load_file_definitions()
        processor.file_definitions = file_definitions
        
        print(f"\n加载file_definitions完成:")
        print(f"  file_definitions: {file_definitions}")
        print(f"  键: {list(file_definitions.keys()) if file_definitions else 'None'}")
        
        # 解析原始文件
        workbook, sheet, first_row, column_data, data_row_count = processor._parse_original_file()
        
        # 处理表头行
        special_first_row = processor._process_header_row(sheet, first_row)
        
        # 按列处理数据
        processed_column_data = processor._process_columns(column_data, data_row_count)
        
        # 检查_generate_result_file方法中的file_definitions
        print(f"\n检查_generate_result_file方法中的file_definitions:")
        print(f"  processor.file_definitions: {processor.file_definitions}")
        print(f"  类型: {type(processor.file_definitions)}")
        
        if processor.file_definitions:
            print(f"  键: {list(processor.file_definitions.keys())}")
            for key in processor.file_definitions:
                print(f"    键: {key}, 键.upper(): {key.upper()}, 是否等于'OUTPUT': {key.upper() == 'OUTPUT'}")
    
    except Exception as e:
        print(f"检查失败: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        db_session.close()
    
    print("\n" + "=" * 100)
    print("检查完成")
    print("=" * 100)

if __name__ == "__main__":
    check_generate_result_file()
