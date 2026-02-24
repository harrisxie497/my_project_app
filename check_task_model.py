"""
查看Task模型结构
"""
import sys
import os
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from app.models.task import Task

print("Task模型的字段:")
for attr in dir(Task):
    if not attr.startswith('_'):
        print(f"  {attr}")

print("\n" + "=" * 80)
print("Task模型的关键属性:")
print("=" * 80)

# 创建一个Task实例来查看属性
from app.core.database import SessionLocal
db = SessionLocal()

task = db.query(Task).filter(Task.file_type == 'DELIVERY').first()

if task:
    print(f"\n找到DELIVERY任务:")
    print(f"  id: {task.id}")
    print(f"  unique_code: {task.unique_code}")
    print(f"  mawb_no: {task.mawb_no}")
    print(f"  flight_no: {task.flight_no}")
    print(f"  arrival_date: {task.arrival_date}")
    print(f"  declare_date: {task.declare_date}")
    print(f"  file_type: {task.file_type}")

else:
    print("\n❌ 未找到DELIVERY任务")

db.close()
