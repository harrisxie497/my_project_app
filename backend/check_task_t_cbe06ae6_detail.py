"""
直接查询任务t_cbe06ae6的详细信息
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.core.database import SessionLocal
from app.models.task import Task

def check_task_detail():
    """查询任务t_cbe06ae6的详细信息"""
    print("=" * 100)
    print("查询任务t_cbe06ae6的详细信息")
    print("=" * 100)
    
    db_session = SessionLocal()
    
    try:
        # 查询任务t_cbe06ae6
        task = db_session.query(Task).filter(Task.id == 't_cbe06ae6').first()
        
        if task:
            print(f"\n任务ID: {task.id}")
            print(f"  文件类型: {task.file_type}")
            print(f"  状态: {task.status}")
            print(f"  错误信息: {task.error}")
            print(f"  创建时间: {task.created_at}")
            print(f"  开始时间: {task.started_at}")
            print(f"  完成时间: {task.finished_at}")
            
            # 从files字段获取任务目录
            files = task.files if task.files else {}
            task_dir = files.get('task_dir', '')
            print(f"  任务目录: {task_dir}")
            
            # 检查任务目录中的文件
            if task_dir and os.path.exists(task_dir):
                print(f"\n任务目录中的文件:")
                for filename in os.listdir(task_dir):
                    filepath = os.path.join(task_dir, filename)
                    if os.path.isfile(filepath):
                        print(f"  {filename}")
            else:
                print(f"\n任务目录不存在: {task_dir}")
        else:
            print("\n未找到任务t_cbe06ae6")
    
    finally:
        db_session.close()
    
    print("\n" + "=" * 100)
    print("查询完成")
    print("=" * 100)

if __name__ == "__main__":
    check_task_detail()
