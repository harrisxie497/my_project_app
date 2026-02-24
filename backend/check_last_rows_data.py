"""
检查原始文件后3行数据的情况
"""

import openpyxl

def check_last_rows_data():
    """检查原始文件后3行数据的情况"""
    print("=" * 100)
    print("检查原始文件后3行数据的情况")
    print("=" * 100)
    
    original_file = r'C:\Users\harris.xie\Documents\trae_projects\japan\backend\storage\tasks\t_fc2fe5d3\original.xlsx'
    
    # 读取原始文件
    workbook = openpyxl.load_workbook(original_file)
    sheet = workbook.active
    
    # 获取表头
    headers = []
    for cell in sheet[1]:
        headers.append(cell.value)
    
    print(f"\n表头: {headers}")
    
    # 获取后3行数据
    print(f"\n后3行数据:")
    for row_idx in range(126, 129):
        print(f"\n行{row_idx}:")
        for col_idx, header in enumerate(headers[:10]):
            cell_value = sheet.cell(row=row_idx, column=col_idx + 1).value
            print(f"  {header}: {cell_value}")
    
    print("\n" + "=" * 100)
    print("检查完成")
    print("=" * 100)

if __name__ == "__main__":
    check_last_rows_data()
