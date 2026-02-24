"""清理测试任务"""
from app.core.database import SessionLocal
from app.models.task import Task

db = SessionLocal()

# 删除测试任务
test_tasks = db.query(Task).filter(Task.id.like('test_%')).all()

print(f"找到{len(test_tasks)}个测试任务")

for task in test_tasks:
    print(f"删除任务: {task.id}")
    db.delete(task)

db.commit()
print("清理完成")
db.close()
