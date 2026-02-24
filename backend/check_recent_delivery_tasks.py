"""
检查所有DELIVERY任务
"""
from app.core.database import SessionLocal
from app.models.task import Task
from datetime import datetime, timedelta

print("=" * 80)
print("检查所有DELIVERY任务")
print("=" * 80)

db = SessionLocal()

try:
    # 查询所有DELIVERY任务
    tasks = db.query(Task).filter(
        Task.file_type == 'DELIVERY'
    ).order_by(Task.created_at.desc()).limit(10).all()
    
    print(f"\n找到 {len(tasks)} 个DELIVERY任务:")
    print("-" * 80)
    
    for idx, task in enumerate(tasks, 1):
        print(f"\n【任务 {idx}】")
        print(f"  ID: {task.id}")
        print(f"  唯一标识码: {task.unique_code}")
        print(f"  状态: {task.status}")
        print(f"  进度阶段: {task.progress_stage}")
        print(f"  进度消息: {task.progress_message}")
        print(f"  创建时间: {task.created_at}")
        
        if task.status == 'FAILED':
            print(f"  错误信息: {task.error}")
        
        # 检查是否包含"553349be"
        if '553349be' in task.id or '553349be' in task.unique_code:
            print("  >>> 找到匹配任务！")
    
    # 如果没有找到DELIVERY任务，查询所有任务
    if not tasks:
        print("\n没有找到DELIVERY任务，查询所有最近任务...")
        print("-" * 80)
        
        all_tasks = db.query(Task).order_by(Task.created_at.desc()).limit(20).all()
        
        print(f"\n找到 {len(all_tasks)} 个任务:")
        for idx, task in enumerate(all_tasks, 1):
            print(f"{idx}. ID: {task.id} | 类型: {task.file_type} | 状态: {task.status} | 创建: {task.created_at}")
            
            # 检查是否包含"553349be"
            if '553349be' in task.id or '553349be' in task.unique_code:
                print("   >>> 找到匹配任务！")
                print(f"   详细信息:")
                print(f"   - 状态: {task.status}")
                print(f"   - 进度阶段: {task.progress_stage}")
                print(f"   - 进度消息: {task.progress_message}")
                print(f"   - 错误: {task.error}")
                print(f"   - 统计: {task.stats}")
                print(f"   - 文件: {task.files}")
    
    print("\n" + "=" * 80)
    
except Exception as e:
    print(f"错误: {str(e)}")
    import traceback
    traceback.print_exc()
finally:
    db.close()
