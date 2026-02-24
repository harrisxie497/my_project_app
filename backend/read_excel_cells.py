"""
直接读取Excel单元格的值和类型
"""
import openpyxl

result_file = "storage/tasks/test_d_column_001/result.xlsx"

print("=" * 80)
print("读取Excel单元格的值和类型")
print("=" * 80)

wb = openpyxl.load_workbook(result_file)
ws = wb.active

print(f"\nD列（時間帯指定）的单元格详情:")
for row_idx in range(2, 8):
    cell = ws.cell(row=row_idx, column=4)
    print(f"\n第{row_idx}行:")
    print(f"  单元格: A{row_idx}")
    print(f"  value: {repr(cell.value)}")
    print(f"  value类型: {type(cell.value).__name__}")
    print(f"  is None: {cell.value is None}")
    print(f"  is 空字符串: {cell.value == ''}")
    print(f"  internal_value: {repr(cell._value)}")

wb.close()
