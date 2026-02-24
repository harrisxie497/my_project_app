"""
运行测试并查看D列的日志
"""
import sys
import os
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from app.core.database import SessionLocal
from app.services.delivery_processor import DeliveryProcessor

# 设置日志级别为DEBUG
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

print("=" * 80)
print("DELIVERY任务测试 - 查看D列日志")
print("=" * 80)

task_dir = "storage/tasks/test_delivery_jkm_001"
result_file = os.path.join(task_dir, "result.xlsx")

db = SessionLocal()

try:
    header_params = {
        'mawb_no': 'TEST-001',
        'flight_no': 'CA123',
        'arrival_date': '2026-02-10'
    }

    print(f"\nHeader params: {header_params}")

    processor = DeliveryProcessor(
        task_dir=task_dir,
        db_session=db,
        file_type='DELIVERY',
        header_params=header_params
    )

    result = processor.process()
    print(f"\n✅ 处理完成")

except Exception as e:
    print(f"\n❌ 处理失败: {str(e)}")
    import traceback
    traceback.print_exc()
finally:
    db.close()

print(f"\n结果文件: {result_file}")
