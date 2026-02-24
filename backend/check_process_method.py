"""
检查process方法中的file_definitions
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.core.database import SessionLocal
from app.services.customs_processor import CustomsProcessor

def check_process_method():
    """检查process方法中的file_definitions"""
    print("=" * 100)
    print("检查process方法中的file_definitions")
    print("=" * 100)
    
    db_session = SessionLocal()
    
    try:
        # 创建CustomsProcessor实例
        task_dir = r'C:\Users\harris.xie\Documents\trae_projects\japan\backend\storage\tasks\t_aa9d170a'
        processor = CustomsProcessor(db_session=db_session, task_dir=task_dir, file_type='CUSTOMS')
        
        print(f"\nCustomsProcessor初始化完成:")
        print(f"  file_type: {processor.file_type}")
        print(f"  file_definitions: {processor.file_definitions}")
        
        # 调用process方法
        stats = processor.process()
        
        print(f"\nprocess方法执行完成:")
        print(f"  统计信息: {stats}")
    
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
    check_process_method()
