"""
检查processed_column_data中的列名
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.core.database import SessionLocal
from app.services.customs_processor import CustomsProcessor

def check_processed_column_data():
    """检查processed_column_data中的列名"""
    print("=" * 100)
    print("检查processed_column_data中的列名")
    print("=" * 100)
    
    db_session = SessionLocal()
    
    try:
        # 创建CustomsProcessor实例
        task_dir = r'C:\Users\harris.xie\Documents\trae_projects\japan\backend\storage\tasks\t_b6617ca6'
        processor = CustomsProcessor(db_session=db_session, task_dir=task_dir, file_type='CUSTOMS')
        
        # 解析原始文件
        workbook, sheet, first_row, column_data, data_row_count = processor._parse_original_file()
        
        # 处理列
        processed_column_data = processor._process_columns(column_data, data_row_count)
        
        print(f"\nprocessed_column_data（共{len(processed_column_data)}列）:")
        for idx, col in enumerate(processed_column_data, start=1):
            print(f"  {idx}. {col['head']}")
    
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
    check_processed_column_data()
