"""
检查任务t_cbe06ae6的日志
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.core.database import SessionLocal
from app.models.task import Task

def check_task_logs():
    """检查任务t_cbe06ae6的日志"""
    print("=" * 100)
    print("检查任务t_cbe06ae6的日志")
    print("=" * 100)
    
    db_session = SessionLocal()
    
    try:
        # 查询任务t_cbe06ae6
        task = db_session.query(Task).filter(Task.id == 't_cbe06ae6').first()
        
        if task:
            print(f"\n任务ID: {task.id}")
            print(f"  文件类型: {task.file_type}")
            print(f"  状态: {task.status}")
            print(f"  错误信息: {task.error_message}")
            print(f"  创建时间: {task.created_at}")
            print(f"  更新时间: {task.updated_at}")
            
            # 从files字段获取任务目录
            files = task.files if task.files else {}
            task_dir = files.get('task_dir', '')
            print(f"  任务目录: {task_dir}")
            
            # 检查日志文件
            log_file = r'C:\Users\harris.xie\Documents\trae_projects\japan\backend\logs\app.log'
            
            # 读取日志文件，查找与该任务相关的日志
            with open(log_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            # 查找与该任务相关的日志
            print(f"\n与任务t_cbe06ae6相关的日志:")
            
            task_logs = []
            for idx, line in enumerate(lines):
                if 't_cbe06ae6' in line:
                    task_logs.append((idx, line.strip()))
            
            if task_logs:
                for idx, log in task_logs[-50:]:  # 只打印最后50条
                    print(f"  行{idx}: {log}")
            else:
                print("  未找到与该任务相关的日志")
            
            # 查找错误日志
            print(f"\n错误日志:")
            
            error_logs = []
            for idx, line in enumerate(lines):
                if 'ERROR' in line or 'error' in line.lower():
                    error_logs.append((idx, line.strip()))
            
            if error_logs:
                for idx, log in error_logs[-20:]:  # 只打印最后20条
                    print(f"  行{idx}: {log}")
            else:
                print("  未找到错误日志")
        else:
            print("\n未找到任务t_cbe06ae6")
    
    finally:
        db_session.close()
    
    print("\n" + "=" * 100)
    print("检查完成")
    print("=" * 100)

if __name__ == "__main__":
    check_task_logs()
