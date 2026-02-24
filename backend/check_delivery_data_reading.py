"""
检查DELIVERY类型任务的原始文件数据读取
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.core.database import SessionLocal
from app.services.delivery_processor import DeliveryProcessor

def check_delivery_data_reading():
    """检查DELIVERY类型任务的原始文件数据读取"""
    print("=" * 100)
    print("检查DELIVERY类型任务的原始文件数据读取")
    print("=" * 100)
    
    db_session = SessionLocal()
    
    try:
        # 创建DeliveryProcessor实例
        task_dir = r'C:\Users\harris.xie\Documents\trae_projects\japan\backend\storage\tasks\t_fc2fe5d3'
        processor = DeliveryProcessor(db_session=db_session, task_dir=task_dir, file_type='DELIVERY')
        
        # 解析原始文件
        workbook, sheet, first_row, column_data, data_row_count = processor._parse_original_file()
        
        print(f"\n解析原始文件完成:")
        print(f"  第一行: {len(first_row)}")
        print(f"  列数: {len(column_data)}")
        print(f"  数据行数: {data_row_count}")
        
        # 检查特定列的数据
        print(f"\n检查特定列的数据:")
        for col in column_data:
            col_header = col.get('head')
            col_data = col.get('data', [])
            if col_header in ['お客様管理番号', '佐川問合せ番号HAWB', '配達指定日', '時間帯指定', '貨物個数', 'お届け先人名', 'お届け先住所', 'お届け先電話', 'お届け先郵便']:
                print(f"  {col_header}: 数据长度={len(col_data)}, 前5个数据={col_data[:5]}")
    
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
    check_delivery_data_reading()
