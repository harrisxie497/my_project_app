"""
检查原始文件读取情况
"""
from app.services.excel_reader import read_excel_file
import json

original_file = "storage/tasks/test_abc_columns_001/original.xlsx"

print("=" * 80)
print("检查原始文件读取")
print("=" * 80)

result = read_excel_file(
    original_file,
    file_type='DELIVERY',
    file_role='SOURCE'
)

print(f"\n工作表: {result['worksheet'].title}")
print(f"第一行: {result['first_row']}")
print(f"数据行数: {result['data_row_count']}")

print("\n列数据:")
for col in result['column_data']:
    print(f"\n  列: {col.get('source_cols')}")
    print(f"  表头: {col.get('head')}")
    print(f"  数据长度: {col.get('len')}")
    print(f"  前5个数据: {col.get('data', [])[:5]}")
