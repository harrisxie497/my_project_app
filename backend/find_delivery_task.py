"""
查找DELIVERY类型的任务
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.core.database import SessionLocal
from app.models.task import Task
from app.models.file_definition import FileDefinition

def find_delivery_task():
    """查找DELIVERY类型的任务"""
    print("=" * 100)
    print("查找DELIVERY类型的任务")
    print("=" * 100)
    
    db_session = SessionLocal()
    
    try:
        # 查询DELIVERY类型的任务
        delivery_task = db_session.query(Task).filter(
            Task.file_type == 'DELIVERY'
        ).order_by(Task.created_at.desc()).first()
        
        if delivery_task:
            print(f"\nDELIVERY类型的任务:")
            print(f"  ID: {delivery_task.id}")
            print(f"  文件类型: {delivery_task.file_type}")
            print(f"  创建时间: {delivery_task.created_at}")
            print(f"  状态: {delivery_task.status}")
        else:
            print(f"\n未找到DELIVERY类型的任务")
        
        # 查询DELIVERY类型的file_definitions
        print(f"\nDELIVERY类型的file_definitions:")
        file_definitions = db_session.query(FileDefinition).filter(
            FileDefinition.file_type == 'DELIVERY'
        ).all()
        
        for fd in file_definitions:
            print(f"\n  file_role: {fd.file_role}")
            print(f"    sheet_name: {fd.sheet_name}")
            print(f"    header_row: {fd.header_row}")
            print(f"    data_start_row: {fd.data_start_row}")
            print(f"    columns_json（共{len(fd.columns_json)}列）:")
            for idx, col in enumerate(fd.columns_json, start=1):
                print(f"      {idx}. {col['col']}: {col['header']}")
    
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
    find_delivery_task()
