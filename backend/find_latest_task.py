"""
查找最新的任务
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.core.database import SessionLocal
from app.models.task import Task

def find_latest_task():
    """查找最新的任务"""
    print("=" * 100)
    print("查找最新的任务")
    print("=" * 100)
    
    db_session = SessionLocal()
    
    try:
        # 查询最新的任务
        latest_task = db_session.query(Task).order_by(Task.created_at.desc()).first()
        
        if latest_task:
            print(f"\n最新的任务:")
            print(f"  ID: {latest_task.id}")
            print(f"  文件类型: {latest_task.file_type}")
            print(f"  创建时间: {latest_task.created_at}")
            print(f"  状态: {latest_task.status}")
        else:
            print(f"\n未找到任务")
    
    except Exception as e:
        print(f"查询失败: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        db_session.close()
    
    print("\n" + "=" * 100)
    print("查找完成")
    print("=" * 100)

if __name__ == "__main__":
    find_latest_task()
