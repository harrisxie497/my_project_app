"""
运行任务t_aa9d170a
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.services.customs_processor import CustomsProcessor
from app.core.database import SessionLocal
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def run_task_t_aa9d170a():
    """运行任务t_aa9d170a"""
    print("=" * 100)
    print("运行任务t_aa9d170a")
    print("=" * 100)
    
    # 任务目录
    task_dir = r'C:\Users\harris.xie\Documents\trae_projects\japan\backend\storage\tasks\t_aa9d170a'
    
    # 创建数据库连接
    db_session = SessionLocal()
    
    # 创建CustomsProcessor实例
    processor = CustomsProcessor(db_session=db_session, task_dir=task_dir, file_type='CUSTOMS')
    
    # 运行任务
    print("\n开始运行任务...")
    try:
        result = processor.process()
        print(f"\n任务运行完成！")
        print(f"结果: {result}")
    except Exception as e:
        print(f"\n任务运行失败: {e}")
        import traceback
        traceback.print_exc()
    
    # 关闭数据库连接
    db_session.close()
    
    print("\n" + "=" * 100)
    print("任务运行完成！")
    print("=" * 100)

if __name__ == "__main__":
    run_task_t_aa9d170a()
