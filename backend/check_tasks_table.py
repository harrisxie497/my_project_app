"""
检查tasks表的结构
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.core.database import SessionLocal
from app.models.task import Task

def check_tasks_table():
    """检查tasks表的结构"""
    print("=" * 100)
    print("检查tasks表的结构")
    print("=" * 100)
    
    db_session = SessionLocal()
    
    try:
        # 查询任务t_fc2fe5d3的信息
        task = db_session.query(Task).filter(
            Task.id == 't_fc2fe5d3'
        ).first()
        
        if task:
            print(f"\n任务t_fc2fe5d3的信息:")
            print(f"  ID: {task.id}")
            print(f"  unique_code: {task.unique_code}")
            print(f"  file_type: {task.file_type}")
            print(f"  status: {task.status}")
            print(f"  created_at: {task.created_at}")
            print(f"  updated_at: {task.updated_at}")
        else:
            print(f"\n未找到任务t_fc2fe5d3")
    
    except Exception as e:
        print(f"查询失败: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        db_session.close()
    
    print("\n" + "=" * 100)
    print("检查完成")
    print("=" * 100)

if __name__ == "__main__":
    check_tasks_table()
