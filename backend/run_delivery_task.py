"""
运行DELIVERY类型任务
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.core.database import SessionLocal
from app.services.delivery_processor import DeliveryProcessor

def run_delivery_task():
    """运行DELIVERY类型任务"""
    print("=" * 100)
    print("运行DELIVERY类型任务")
    print("=" * 100)
    
    db_session = SessionLocal()
    
    try:
        # 创建DeliveryProcessor实例
        task_dir = r'C:\Users\harris.xie\Documents\trae_projects\japan\backend\storage\tasks\t_fc2fe5d3'
        header_params = {'mawb_no': '160-03270890', 'flight_no': '', 'arrival_date': ''}
        processor = DeliveryProcessor(db_session=db_session, task_dir=task_dir, file_type='DELIVERY', header_params=header_params)
        
        # 运行任务
        stats = processor.process()
        
        print(f"\n任务运行完成:")
        print(f"  统计信息: {stats}")
    
    except Exception as e:
        print(f"任务运行失败: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        db_session.close()
    
    print("\n" + "=" * 100)
    print("任务运行完成")
    print("=" * 100)

if __name__ == "__main__":
    run_delivery_task()
