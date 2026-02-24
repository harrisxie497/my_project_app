"""
检查数据处理过程中的数据长度
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.core.database import SessionLocal
from app.services.customs_processor import CustomsProcessor

def check_data_processing():
    """检查数据处理过程中的数据长度"""
    print("=" * 100)
    print("检查数据处理过程中的数据长度")
    print("=" * 100)
    
    db_session = SessionLocal()
    
    try:
        # 创建CustomsProcessor实例
        task_dir = r'C:\Users\harris.xie\Documents\trae_projects\japan\backend\storage\tasks\t_b6617ca6'
        processor = CustomsProcessor(db_session=db_session, task_dir=task_dir, file_type='CUSTOMS')
        
        # 解析原始文件
        workbook, sheet, first_row, column_data, data_row_count = processor._parse_original_file()
        
        print(f"\n解析原始文件完成:")
        print(f"  第一行: {len(first_row)}")
        print(f"  列数: {len(column_data)}")
        print(f"  数据行数: {data_row_count}")
        
        # 检查特定列的数据长度
        print(f"\n检查特定列的数据长度:")
        for col in column_data:
            col_header = col.get('head')
            col_data = col.get('data', [])
            if col_header in ['輸入者電話番号', '收件人电话']:
                print(f"  {col_header}: 数据长度={len(col_data)}, 数据={col_data}")
    
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
    check_data_processing()
