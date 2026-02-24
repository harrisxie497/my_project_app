"""
检查原始文件中D列的值
"""
from app.services.excel_reader import read_excel_file

original_file = "storage/tasks/test_d_column_001/original.xlsx"

print("=" * 80)
print("检查原始文件中D列的值")
print("=" * 80)

result = read_excel_file(original_file, file_type='DELIVERY', file_role='SOURCE')

print(f"\n数据行数: {result['data_row_count']}")

print("\n原始D列数据:")
for col in result['column_data']:
    if col.get('head') == '時間帯指定':
        data = col.get('data')
        print(f"  数据长度: {len(data)}")
        print(f"  数据内容: {data}")
        for idx, val in enumerate(data, start=2):
            print(f"    第{idx}行: {repr(val)} (类型: {type(val).__name__})")

print("\n原始C列数据:")
for col in result['column_data']:
    if col.get('head') == '配達指定日':
        data = col.get('data')
        print(f"  数据长度: {len(data)}")
        print(f"  数据内容: {data}")
        for idx, val in enumerate(data, start=2):
            print(f"    第{idx}行: {repr(val)} (类型: {type(val).__name__})")
