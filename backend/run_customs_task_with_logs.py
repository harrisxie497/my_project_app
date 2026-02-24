"""
运行CUSTOMS任务测试
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.core.database import SessionLocal
from app.services.customs_processor import CustomsProcessor

def run_customs_task():
    """运行CUSTOMS任务测试"""
    print("=" * 100)
    print("运行CUSTOMS任务测试")
    print("=" * 100)
    
    db_session = SessionLocal()
    
    try:
        # 创建CustomsProcessor实例
        task_dir = r'C:\Users\harris.xie\Documents\trae_projects\japan\backend\storage\tasks\t_aa9d170a'
        header_params = {'mawb_no': '160-03270890', 'flight_no': '', 'arrival_date': ''}
        processor = CustomsProcessor(db_session=db_session, task_dir=task_dir, file_type='CUSTOMS', header_params=header_params)
        
        # 执行处理
        result = processor.process()
        
        print(f"\n处理完成:")
        print(f"  结果文件: {result.get('output_file') if result else None}")
        print(f"  统计信息: {result.get('stats') if result else None}")
    
    except Exception as e:
        print(f"处理失败: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db_session.close()

if __name__ == "__main__":
    run_customs_task()
