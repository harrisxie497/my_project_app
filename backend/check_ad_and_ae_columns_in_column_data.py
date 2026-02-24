"""
检查column_data中是否有AD和AE列的数据
"""

from app.services.excel_reader import read_excel_file
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def check_ad_and_ae_columns_in_column_data():
    """检查column_data中是否有AD和AE列的数据"""
    print("=" * 100)
    print("检查column_data中是否有AD和AE列的数据")
    print("=" * 100)
    
    # 原始文件路径
    original_file_path = r'C:\Users\harris.xie\Documents\trae_projects\japan\backend\storage\tasks\t_aa9d170a\original.xlsx'
    
    # 文件类型
    file_type = 'CUSTOMS'
    
    # 读取Excel文件
    print(f"\n读取Excel文件...")
    result = read_excel_file(
        original_file_path,
        sheet_name=None,
        file_type=file_type,
        file_role='SOURCE'
    )
    
    column_data = result["column_data"]
    data_row_count = result["data_row_count"]
    
    print(f"\n数据行数: {data_row_count}")
    print(f"列数: {len(column_data)}")
    
    # 检查AD和AE列的数据
    columns_to_check = ['AD', 'AE']
    
    print(f"\n检查AD和AE列的数据:")
    for col_letter in columns_to_check:
        found = False
        for col in column_data:
            col_source_cols = col.get('source_cols')
            if col_source_cols == col_letter:
                found = True
                print(f"\n{col_letter}列:")
                print(f"  col: {col.get('source_cols')}")
                print(f"  head: {col.get('head')}")
                print(f"  data长度: {len(col.get('data', []))}")
                print(f"  前5行数据: {col.get('data', [])[:5]}")
                break
        
        if not found:
            print(f"\n❌ {col_letter}列未在column_data中找到")
    
    print("\n" + "=" * 100)
    print("检查完成！")
    print("=" * 100)

if __name__ == "__main__":
    check_ad_and_ae_columns_in_column_data()
