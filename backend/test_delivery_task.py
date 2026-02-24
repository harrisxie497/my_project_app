"""
测试DELIVERY任务处理器
"""
import sys
import os
from datetime import datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.database import get_db
from app.models.task import Task
from app.models.field_pipeline import FieldPipeline
from app.models.file_definition import FileDefinition
from app.services.delivery_processor import DeliveryProcessor

print("=" * 80)
print("测试DELIVERY任务处理器")
print("=" * 80)

# 获取数据库会话
db = next(get_db())

# 查询DELIVERY任务
tasks = db.query(Task).filter(Task.file_type == 'DELIVERY').all()

if not tasks:
    print("\n❌ 没有找到DELIVERY任务")
    print("请先创建一个DELIVERY任务")
    db.close()
    sys.exit(1)

print(f"\n找到 {len(tasks)} 个DELIVERY任务:")
for t in tasks:
    print(f"  ID: {t.id}, 状态: {t.status}, 输入文件: {t.input_file_path}")

# 选择第一个任务进行测试
task = tasks[0]
print(f"\n选择任务 ID: {task.id}")

# 获取任务目录
task_dir = os.path.dirname(task.input_file_path) if task.input_file_path else None
print(f"任务目录: {task_dir}")

# 查询field_pipelines配置
pipelines = db.query(FieldPipeline).filter(FieldPipeline.file_type == 'DELIVERY').all()
print(f"\nField pipelines配置数量: {len(pipelines)}")

# 查询file_definitions配置
file_defs = db.query(FileDefinition).filter(FileDefinition.file_type == 'DELIVERY').all()
print(f"File definitions配置数量: {len(file_defs)}")

for file_def in file_defs:
    print(f"  - 文件类型: {file_def.file_type}, 用途: {file_def.file_usage}, 工作表: {file_def.sheet_name}")

# 更新任务状态为处理中
task.status = 'processing'
task.started_at = datetime.now()
db.commit()
print(f"\n✅ 任务状态更新为: {task.status}")

# 初始化处理器
header_params = {
    'mawb_no': task.mawb_no or 'TEST001',
    'flight_no': task.flight_no or 'CA123',
    'arrival_date': task.arrival_date.strftime('%Y-%m-%d') if task.arrival_date else '2026-02-10'
}

processor = DeliveryProcessor(
    task_dir=task_dir,
    db_session=db,
    file_type='DELIVERY',
    header_params=header_params
)

print(f"\n处理器初始化完成")
print(f"Header params: {header_params}")

# 执行处理
try:
    print("\n" + "=" * 80)
    print("开始执行任务处理...")
    print("=" * 80)

    result = processor.process()

    print("\n" + "=" * 80)
    print("✅ 任务处理完成")
    print("=" * 80)
    print(f"处理结果: {result}")

    # 更新任务状态为完成
    task.status = 'completed'
    task.completed_at = datetime.now()
    task.result_file_path = processor.result_file_path
    db.commit()
    print(f"\n✅ 任务状态更新为: {task.status}")
    print(f"结果文件: {task.result_file_path}")

    # 检查结果文件是否存在
    if task.result_file_path and os.path.exists(task.result_file_path):
        file_size = os.path.getsize(task.result_file_path)
        print(f"结果文件大小: {file_size} 字节")
    else:
        print("❌ 结果文件不存在")

except Exception as e:
    print(f"\n❌ 任务处理失败: {e}")
    import traceback
    traceback.print_exc()

    # 更新任务状态为失败
    task.status = 'failed'
    task.error_message = str(e)
    task.completed_at = datetime.now()
    db.commit()
    print(f"\n任务状态更新为: {task.status}")
    print(f"错误信息: {task.error_message}")

finally:
    db.close()
    print("\n测试完成！")
