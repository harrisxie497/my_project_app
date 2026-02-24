"""
测试DELIVERY任务创建和执行
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
print("DELIVERY任务创建和执行测试")
print("=" * 80)

db = SessionLocal()

try:
    # 1. 检查测试文件是否存在
    test_file = os.path.join(os.path.dirname(__file__), "test_results", "delivery_original.xlsx")
    if not os.path.exists(test_file):
        print(f"[FAIL] 测试文件不存在: {test_file}")
        print(f"当前工作目录: {os.getcwd()}")
        print(f"脚本所在目录: {os.path.dirname(__file__)}")
        # 列出test_results目录内容
        results_dir = os.path.join(os.path.dirname(__file__), "test_results")
        if os.path.exists(results_dir):
            print(f"test_results目录内容: {os.listdir(results_dir)}")
        print("请先运行 create_delivery_test_file.py 创建测试文件")
        sys.exit(1)
    
    print(f"[OK] 测试文件存在: {test_file}")
    
    # 2. 创建新任务
    print("\n【创建DELIVERY任务】")
    task_unique_code = f"TEST_DELIVERY_{datetime.now().strftime('%Y%m%d%H%M%S')}"
    task_id = str(uuid.uuid4())
    
    new_task = Task(
        id=task_id,
        file_type='DELIVERY',
        unique_code=task_unique_code,
        created_by_user_id='system-test',
        header_params='{}',
        status='queued'
    )
    
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    
    print(f"[OK] 任务创建成功")
    print(f"  任务ID: {new_task.id}")
    print(f"  unique_code: {new_task.unique_code}")
    print(f"  file_type: {new_task.file_type}")
    print(f"  status: {new_task.status}")
    
    # 3. 测试直接创建Processor（简化测试，不测试Excel读取）
    
    # 4. 测试TaskExecutor（使用正确的参数顺序）
    print("\n【测试TaskExecutor】")
    try:
        # 根据代码，应该是 (task_id, db_session) 或 (task_id, file_type, db_session)
        # 让我们尝试两种方式
        executor = TaskExecutor(db, new_task.id, 'DELIVERY')
        print(f"[OK] TaskExecutor创建成功")
        
        # 加载配置
        executor._load_task_record()
        print(f"[OK] 任务记录加载成功")
        
        executor._load_configurations()
        print(f"[OK] 配置加载成功")
        print(f"  file_definitions: {len(executor.file_definitions) if executor.file_definitions else 0}")
        print(f"  field_pipelines: {len(executor.field_pipelines) if executor.field_pipelines else 0}")
        
    except Exception as e:
        print(f"[FAIL] TaskExecutor测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 80)
    print("测试完成")
    print("=" * 80)
    
except Exception as e:
    print(f"错误: {str(e)}")
    import traceback
    traceback.print_exc()
finally:
    db.close()
