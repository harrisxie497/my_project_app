"""
检查任务 t_b1d6559d 的详细信息和错误日志
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.core.database import SessionLocal
from app.models.task import Task

def check_task_detail():
    """检查任务 t_b1d6559d 的详细信息"""
    print("=" * 100)
    print("检查任务 t_b1d6559d 的详细信息")
    print("=" * 100)
    
    db_session = SessionLocal()
    
    try:
        # 查询任务 t_b1d6559d
        task = db_session.query(Task).filter(
            Task.id == 't_b1d6559d'
        ).first()
        
        if task:
            print(f"\n任务ID: {task.id}")
            print(f"  文件类型: {task.file_type}")
            print(f"  状态: {task.status}")
            print(f"  进度消息: {task.progress_message}")
            print(f"  创建时间: {task.created_at}")
            
            # 打印files字段
            print(f"  Files: {task.files}")
            
            # 从files字段获取任务目录
            files = task.files if task.files else {}
            task_dir = files.get('task_dir', '')
            print(f"  任务目录: {task_dir}")
            
            # 检查日志文件
            if task_dir:
                log_file = os.path.join(task_dir, 'task.log')
                if os.path.exists(log_file):
                    print(f"\n任务日志文件: {log_file}")
                    print("\n日志内容:")
                    with open(log_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                        print(content)
                else:
                    print(f"\n任务日志文件不存在: {log_file}")
        else:
            print("\n未找到任务 t_b1d6559d")
    
    finally:
        db_session.close()
    
    print("\n" + "=" * 100)
    print("检查完成")
    print("=" * 100)

if __name__ == "__main__":
    check_task_detail()
