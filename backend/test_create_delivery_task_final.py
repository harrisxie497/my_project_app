"""测试创建DELIVERY任务（最终版）"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.core.database import SessionLocal
from app.models.task import Task, TaskStatus, FileType
from app.services.task_executor import TaskExecutor
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def test_create_delivery_task():
    """测试创建DELIVERY任务"""
    print("=" * 100)
    print("测试创建DELIVERY任务")
    print("=" * 100)

    db = SessionLocal()

    try:
        # 检查file_definitions是否存在
        from app.models.file_definition import FileDefinition
        file_def = db.query(FileDefinition).filter(
            FileDefinition.file_type == 'DELIVERY',
            FileDefinition.file_role == 'SOURCE'
        ).first()

        if not file_def:
            print(f"[FAIL] DELIVERY SOURCE file_definition不存在")
            return False

        print(f"[OK] DELIVERY SOURCE file_definition存在")
        print(f"  sheet_name: {file_def.sheet_name}")
        print(f"  header_row: {file_def.header_row}")
        print(f"  data_start_row: {file_def.data_start_row}")

        # 处理columns_json（可能是dict或str）
        import json
        columns = file_def.columns_json
        if isinstance(columns, str):
            columns = json.loads(columns)
        print(f"  columns: {len(columns)}列")

        # 检查field_pipelines是否存在
        from app.models.field_pipeline import FieldPipeline
        pipelines = db.query(FieldPipeline).filter(
            FieldPipeline.file_type == 'DELIVERY'
        ).count()

        if pipelines == 0:
            print(f"[FAIL] DELIVERY field_pipelines不存在")
            return False

        print(f"[OK] DELIVERY field_pipelines存在，共{pipelines}个")

        # 创建测试任务
        import uuid
        task_id = f"test_delivery_{uuid.uuid4().hex[:8]}"
        task = Task(
            id=task_id,
            created_by_user_id=1,
            file_type=FileType.DELIVERY,
            unique_code="TEST001",
            flight_no=None,  # DELIVERY不需要
            declare_date=None,  # DELIVERY不需要
            header_params='{"mawb_no": "MAWB20260207001", "flight_no": "JL123", "arrival_date": "2026-02-08"}',
            status=TaskStatus.QUEUED,
            files={}
        )

        db.add(task)
        db.commit()
        db.refresh(task)

        print(f"[OK] 任务创建成功 - task_id: {task_id}")

        # 检查任务是否可以正确加载
        loaded_task = db.query(Task).filter(Task.id == task_id).first()
        if loaded_task:
            print(f"[OK] 任务加载成功")
            print(f"  file_type: {loaded_task.file_type}")
            print(f"  status: {loaded_task.status}")
            print(f"  header_params: {loaded_task.header_params}")
        else:
            print(f"[FAIL] 任务加载失败")
            return False

        # 尝试创建TaskExecutor
        try:
            executor = TaskExecutor(db, loaded_task.id, 'DELIVERY')
            print(f"[OK] TaskExecutor创建成功")
        except Exception as e:
            print(f"[FAIL] TaskExecutor创建失败: {str(e)}")
            import traceback
            traceback.print_exc()
            return False

        # 尝试初始化处理器（不执行完整流程）
        try:
            executor._load_task_record()
            executor._load_configurations()
            print(f"[OK] 配置加载成功")
            print(f"  file_definitions: {len(executor.file_definitions) if executor.file_definitions else 0}")
            print(f"  field_pipelines: {len(executor.field_pipelines) if executor.field_pipelines else 0}")
        except Exception as e:
            print(f"[FAIL] 配置加载失败: {str(e)}")
            import traceback
            traceback.print_exc()
            return False

        # 清理测试任务
        db.delete(loaded_task)
        db.commit()
        print(f"[OK] 测试任务已清理")

        print("\n" + "=" * 100)
        print("DELIVERY任务创建测试完成!")
        print("=" * 100)
        return True

    except Exception as e:
        print(f"[ERROR] 测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

    finally:
        db.close()

if __name__ == "__main__":
    success = test_create_delivery_task()
    sys.exit(0 if success else 1)
