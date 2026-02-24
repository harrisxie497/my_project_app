"""
运行测试并查看日志
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.core.database import SessionLocal
from app.services.delivery_processor import DeliveryProcessor

# 测试任务目录
task_dir = "storage/tasks/test_d_column_001"

# 创建数据库会话
db = SessionLocal()

try:
    print("处理文件...")
    header_params = {
        'mawb_no': '160-03270890',
        'flight_no': 'CA123',
        'arrival_date': '2026-02-10'
    }

    processor = DeliveryProcessor(
        task_dir=task_dir,
        db_session=db,
        file_type='DELIVERY',
        header_params=header_params
    )

    result = processor.process()
    print(f"处理完成: {result['output_file']}")

except Exception as e:
    print(f"错误: {str(e)}")
finally:
    db.close()

# 读取日志文件
print("\n" + "=" * 80)
print("查看日志文件")
print("=" * 80)

log_file = "backend/logs/app.log.2"
if os.path.exists(log_file):
    with open(log_file, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()
        for line in lines[-200:]:
            if 'D列' in line or '処理D列' in line or 'DEBUG.*D列' in line:
                print(line.strip())
