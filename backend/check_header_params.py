"""
检查header_params的值
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.core.database import SessionLocal
from app.services.delivery_processor import DeliveryProcessor

def check_header_params():
    """检查header_params的值"""
    print("=" * 100)
    print("检查header_params的值")
    print("=" * 100)
    
    db_session = SessionLocal()
    
    try:
        # 创建DeliveryProcessor实例
        task_dir = r'C:\Users\harris.xie\Documents\trae_projects\japan\backend\storage\tasks\t_fc2fe5d3'
        processor = DeliveryProcessor(db_session=db_session, task_dir=task_dir, file_type='DELIVERY')
        
        print(f"\nheader_params的值:")
        print(f"  {processor.header_params}")
    
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
    check_header_params()
