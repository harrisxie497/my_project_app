"""
调试None值替换逻辑
"""
import sys
import os
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from app.core.database import SessionLocal
from app.services.delivery_processor import DeliveryProcessor
import json

task_dir = "storage/tasks/test_delivery_jkm_001"
db = SessionLocal()

header_params = {
    'mawb_no': 'TEST-001',
    'flight_no': 'CA123',
    'arrival_date': '2026-02-10'
}

processor = DeliveryProcessor(
    task_dir=task_dir,
    db_session=db,
    file_type='DELIVERY',
    header_params=header_params
)

# 只执行到按列处理完成，查看processed_column_data
from app.services.excel_reader import read_excel_file

# 1. 解析原始文件
workbook, sheet, first_row, column_data, data_row_count = processor._parse_original_file()

# 2. 处理表头行
special_first_row = None

# 3. 按列处理数据
processed_column_data = processor._process_columns(column_data, data_row_count)

print("\n" + "=" * 80)
print("检查processed_column_data中的None值")
print("=" * 80)

for col in processed_column_data:
    col_name = col['head']
    col_data = col['data']

    # 检查None值
    none_count = sum(1 for v in col_data if v is None)
    empty_string_count = sum(1 for v in col_data if v == '')

    if none_count > 0:
        print(f"\n列 {col_name}:")
        print(f"  总数据: {len(col_data)}")
        print(f"  None值: {none_count}")
        print(f"  空字符串: {empty_string_count}")

        # 显示前5个None值的示例
        none_indices = [i for i, v in enumerate(col_data) if v is None]
        print(f"  前5个None值的行号: {[i+2 for i in none_indices[:5]]}")

total_none = sum(sum(1 for v in col['data'] if v is None) for col in processed_column_data)
print(f"\n总计None值: {total_none}")

db.close()
