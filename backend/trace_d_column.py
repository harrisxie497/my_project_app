"""
追踪D列的完整处理过程
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.core.database import SessionLocal
from app.services.delivery_processor import DeliveryProcessor

# 临时修改excel_writer.py以添加调试日志
import app.services.excel_writer as excel_writer_module

# 保存原始的write_excel_file_by_columns函数
original_write_excel_file_by_columns = excel_writer_module.write_excel_file_by_columns

# 创建一个包装函数来添加调试日志
def debug_write_excel_file_by_columns(file_path, headers, column_data, special_first_row=None):
    print("\n[DEBUG] write_excel_file_by_columns被调用")
    print(f"  file_path: {file_path}")
    print(f"  headers: {headers}")
    print(f"  column_data keys: {list(column_data.keys())}")

    if '時間帯指定' in column_data:
        d_values = column_data['時間帯指定']
        print(f"  D列（時間帯指定）数据: {d_values}")
        print(f"  D列数据长度: {len(d_values)}")
        for idx, val in enumerate(d_values, start=2):
            print(f"    第{idx}行: {repr(val)} (类型: {type(val).__name__})")

    # 调用原始函数
    return original_write_excel_file_by_columns(file_path, headers, column_data, special_first_row)

# 替换函数
excel_writer_module.write_excel_file_by_columns = debug_write_excel_file_by_columns

print("=" * 80)
print("追踪D列的完整处理过程")
print("=" * 80)

# 测试任务目录
task_dir = "storage/tasks/test_d_column_001"

# 创建数据库会话
db = SessionLocal()

try:
    print("\n【步骤1】处理文件")
    print("-" * 80)

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

    print("\n【步骤2】检查结果文件")
    print("-" * 80)

    import openpyxl
    wb = openpyxl.load_workbook(result['output_file'])
    ws = wb.active

    print("\nD列（時間帯指定）的结果值:")
    for row_idx in range(2, 8):
        cell = ws.cell(row=row_idx, column=4)
        print(f"  第{row_idx}行: {repr(cell.value)} (类型: {type(cell.value).__name__})")

    wb.close()

except Exception as e:
    print(f"\n错误: {str(e)}")
    import traceback
    traceback.print_exc()
finally:
    db.close()

# 恢复原始函数
excel_writer_module.write_excel_file_by_columns = original_write_excel_file_by_columns
