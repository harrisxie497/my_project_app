"""
端到端测试：从处理到写入Excel
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.services.field_handlers import calc_time_slot_with_delivery_date
from app.services.excel_writer import write_excel_file_by_columns

print("=" * 80)
print("端到端测试：D列处理和写入")
print("=" * 80)

# 测试数据
test_c_values = ['2026-02-10', '2026-02-11', '2026-02-12', '', '', '']
test_d_values = [0, 5, 12, 0, 8, 15]

print("\n原始数据:")
for i in range(len(test_d_values)):
    print(f"  第{i+2}行: C={repr(test_c_values[i])}, D={test_d_values[i]}")

# 处理D列
processed_d_values = []
for i in range(len(test_d_values)):
    d_val = test_d_values[i]
    c_val = test_c_values[i]
    processed_val = calc_time_slot_with_delivery_date(d_val, c_val)
    processed_d_values.append(processed_val)

print("\n处理后的D列数据:")
for i, val in enumerate(processed_d_values, start=2):
    print(f"  第{i}行: {repr(val)} (类型: {type(val).__name__})")

# 写入Excel
headers = [
    "お客様管理番号", "佐川問合せ番号HAWB", "配達指定日", "時間帯指定", "貨物個数"
]

column_data = {
    "お客様管理番号": ["1", "2", "3", "4", "5", "6"],
    "佐川問合せ番号HAWB": ["SG1", "SG2", "SG3", "SG4", "SG5", "SG6"],
    "配達指定日": test_c_values,
    "時間帯指定": processed_d_values,
    "貨物個数": [1, 2, 1, 1, 2, 1]
}

test_output_file = "test_end_to_end_result.xlsx"
write_excel_file_by_columns(test_output_file, headers, column_data)

# 读取并验证
import openpyxl
wb = openpyxl.load_workbook(test_output_file)
ws = wb.active

print("\n验证结果文件中的D列:")
for i in range(len(processed_d_values)):
    row_idx = i + 2
    cell = ws.cell(row=row_idx, column=4)
    expected = processed_d_values[i]
    actual = cell.value
    print(f"  第{row_idx}行: 期望={repr(expected)}, 实际={repr(actual)}, 类型={type(actual).__name__}")

wb.close()
os.remove(test_output_file)

print("\n测试完成！")
