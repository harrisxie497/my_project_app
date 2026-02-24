"""
清理测试任务
"""
from app.core.database import SessionLocal
from app.models.task import Task

db = SessionLocal()

try:
    # 删除所有TEST_DELIVERY开头的任务
    test_tasks = db.query(Task).filter(
        Task.unique_code.like('TEST_DELIVERY%')
    ).all()
    
    count = len(test_tasks)
    for task in test_tasks:
        db.delete(task)
    
    db.commit()
    print(f"已删除 {count} 个测试任务")
    
except Exception as e:
    print(f"错误: {str(e)}")
    db.rollback()
finally:
    db.close()
