import sys
import os
from datetime import datetime

# 添加backend目录到路径
backend_path = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.insert(0, backend_path)

from app.database import get_db
from app.models.task import Task

print("=" * 80)
print("检查数据库中的DELIVERY任务")
print("=" * 80)

# 获取数据库会话
db = next(get_db())

# 查询所有任务
tasks = db.query(Task).all()

print(f"\n数据库中共有 {len(tasks)} 个任务:\n")

# 按类型分组
from collections import defaultdict
tasks_by_type = defaultdict(list)
for t in tasks:
    tasks_by_type[t.file_type].append(t)

for file_type, type_tasks in tasks_by_type.items():
    print(f"【{file_type}】任务 ({len(type_tasks)} 个):")
    for t in type_tasks[:5]:  # 只显示前5个
        print(f"  ID: {t.id}, 状态: {t.status}")
        if t.input_file_path:
            print(f"    输入: {t.input_file_path}")
        if t.result_file_path:
            print(f"    结果: {t.result_file_path}")
    print()

# 查询DELIVERY任务
delivery_tasks = db.query(Task).filter(Task.file_type == 'DELIVERY').all()

print("=" * 80)
print(f"DELIVERY任务详情 ({len(delivery_tasks)} 个):")
print("=" * 80)

for t in delivery_tasks:
    print(f"\n任务 ID: {t.id}")
    print(f"  状态: {t.status}")
    print(f"  输入文件: {t.input_file_path}")
    print(f"  结果文件: {t.result_file_path}")
    print(f"  MAWB编号: {t.mawb_no}")
    print(f"  航班号: {t.flight_no}")
    print(f"  到港日期: {t.arrival_date}")
    print(f"  创建时间: {t.created_at}")
    if t.error_message:
        print(f"  错误信息: {t.error_message}")

db.close()
print("\n检查完成！")
