"""
测试修复后的DELIVERY任务处理
"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.database import SessionLocal
from app.models.task import Task
from app.services.task_executor import TaskExecutor
from datetime import datetime
import uuid

print("=" * 80)
print("测试修复后的DELIVERY任务处理")
print("=" * 80)

db = SessionLocal()

try:
    # 测试文件路径
    test_file = os.path.join(
        os.path.dirname(__file__),
        "test_results",
        "delivery_original.xlsx"
    )
    
    if not os.path.exists(test_file):
        print(f"[FAIL] 测试文件不存在: {test_file}")
        sys.exit(1)
    
    print(f"[OK] 测试文件存在: {test_file}")
    
    # 创建测试任务
    task_id = f"t_{uuid.uuid4().hex[:8]}"
    task = Task(
        id=task_id,
        file_type='DELIVERY',
        unique_code='160-03270890',  # 使用与失败任务相同的unique_code
        created_by_user_id='test_user',
        header_params='{}',
        status='QUEUED'
    )
    
    db.add(task)
    db.commit()
    db.refresh(task)
    
    print(f"\n[OK] 测试任务创建成功")
    print(f"  任务ID: {task.id}")
    print(f"  unique_code: {task.unique_code}")
    
    # 使用TaskExecutor处理任务
    output_path = os.path.join(
        os.path.dirname(__file__),
        "test_results",
        f"delivery_output_{task.id}.xlsx"
    )
    
    print(f"\n【开始处理任务】")
    print("-" * 80)
    
    executor = TaskExecutor(db, task_id, 'DELIVERY')
    
    # 执行任务
    result = executor.execute(test_file, output_path)
    
    print(f"\n[OK] 任务执行成功")
    print(f"  输出文件: {result.get('output_file')}")
    print(f"  统计信息: {result.get('stats')}")
    
    # 检查输出文件
    if os.path.exists(output_path):
        print(f"\n[OK] 输出文件已生成: {output_path}")
        print(f"  文件大小: {os.path.getsize(output_path)} bytes")
    else:
        print(f"\n[FAIL] 输出文件未生成")
    
    print("\n" + "=" * 80)
    print("测试完成！")
    print("=" * 80)
    
except Exception as e:
    print(f"\n[FAIL] 测试失败: {str(e)}")
    import traceback
    traceback.print_exc()
    
    # 更新任务状态为失败
    if 'task' in locals():
        task.status = 'FAILED'
        task.error = str(e)
        task.progress_message = f"Task failed: {str(e)}"
        task.finished_at = datetime.now()
        db.commit()
        print(f"\n任务状态已更新为失败")
        print(f"  错误信息: {str(e)}")
    
finally:
    db.close()
