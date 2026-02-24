"""
测试处理用户上传的文件
"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.database import SessionLocal
from app.models.task import Task
from app.services.task_executor import TaskExecutor
import uuid

print("=" * 80)
print("测试处理用户上传的文件")
print("=" * 80)

db = SessionLocal()

try:
    # 用户上传的文件路径
    user_file = r"C:\Users\harris.xie\Documents\trae_projects\japan\backend\storage\tasks\t_ec161292\original.xlsx"
    
    if not os.path.exists(user_file):
        print(f"[FAIL] 文件不存在: {user_file}")
        sys.exit(1)
    
    print(f"[OK] 文件存在: {user_file}")
    
    # 创建测试任务
    task_id = f"t_{uuid.uuid4().hex[:8]}"
    task = Task(
        id=task_id,
        file_type='DELIVERY',
        unique_code='160-03270890',
        created_by_user_id='u_5d320783',
        header_params='{}',
        status='QUEUED'
    )
    
    db.add(task)
    db.commit()
    db.refresh(task)
    
    print(f"\n[OK] 测试任务创建成功")
    print(f"  任务ID: {task.id}")
    
    # 输出路径
    output_path = os.path.join(
        os.path.dirname(user_file),
        "result_test.xlsx"
    )
    
    print(f"\n【开始处理任务】")
    print("-" * 80)
    
    # 使用TaskExecutor处理
    executor = TaskExecutor(db, task_id, 'DELIVERY')
    
    result = executor.execute(user_file, output_path)
    
    print(f"\n[OK] 任务执行成功")
    print(f"  输出文件: {result.get('output_file')}")
    print(f"  统计信息: {result.get('stats')}")
    
    # 检查输出文件
    if os.path.exists(result.get('output_file')):
        print(f"\n[OK] 输出文件已生成")
    else:
        print(f"\n[WARN] 输出文件未生成")
    
    print("\n" + "=" * 80)
    print("测试完成！")
    print("=" * 80)
    
except Exception as e:
    print(f"\n[FAIL] 测试失败: {str(e)}")
    import traceback
    traceback.print_exc()
    
    # 更新任务状态
    if 'task' in locals():
        task.status = 'FAILED'
        task.error = str(e)
        task.progress_message = f"Task failed: {str(e)}"
        task.finished_at = task.finished_at or __import__('datetime').datetime.now()
        db.commit()
    
finally:
    db.close()
