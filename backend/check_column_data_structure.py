"""
检查column_data的结构
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.core.database import SessionLocal
from app.services.delivery_processor import DeliveryProcessor

def check_column_data_structure():
    """检查column_data的结构"""
    print("=" * 100)
    print("检查column_data的结构")
    print("=" * 100)
    
    db_session = SessionLocal()
    
    try:
        # 创建DeliveryProcessor实例
        task_dir = r'C:\Users\harris.xie\Documents\trae_projects\japan\backend\storage\tasks\t_fc2fe5d3'
        processor = DeliveryProcessor(db_session=db_session, task_dir=task_dir, file_type='DELIVERY')
        
        # 解析原始文件
        workbook, sheet, first_row, column_data, data_row_count = processor._parse_original_file()
        
        print(f"\ncolumn_data的结构:")
        for idx, col in enumerate(column_data, start=1):
            print(f"\n  {idx}. 列信息:")
            print(f"     head: {col.get('head')}")
            print(f"     source_cols: {col.get('source_cols')}")
            print(f"     data长度: {len(col.get('data', []))}")
            print(f"     data前5个: {col.get('data', [])[:5]}")
    
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
    check_column_data_structure()
