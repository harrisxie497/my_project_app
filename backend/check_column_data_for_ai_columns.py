"""
检查column_data的结构，看看X、Y、J、K列的source_cols是否在column_data中
"""

from app.services.excel_reader import read_excel_file
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def check_column_data_for_ai_columns():
    """检查column_data的结构"""
    print("=" * 100)
    print("检查column_data的结构")
    print("=" * 100)
    
    # 原始文件路径
    original_file_path = r'C:\Users\harris.xie\Documents\trae_projects\japan\backend\storage\tasks\t_aa9d170a\original.xlsx'
    
    # 文件类型
    file_type = 'CUSTOMS'
    
    # 读取Excel文件
    print(f"\n读取Excel文件...")
    result = read_excel_file(original_file_path, file_type, 'SOURCE')
    
    column_data = result["column_data"]
    data_row_count = result["data_row_count"]
    
    print(f"\n数据行数: {data_row_count}")
    print(f"列数: {len(column_data)}")
    
    # 检查AI列的source_cols是否在column_data中
    ai_columns_config = [
        {'target_col': 'X', 'source_cols': ['AD'], 'depends_on': []},
        {'target_col': 'Y', 'source_cols': ['M'], 'depends_on': []},
        {'target_col': 'J', 'source_cols': ['K'], 'depends_on': ['X']},
        {'target_col': 'K', 'source_cols': ['N'], 'depends_on': ['Y']}
    ]
    
    print(f"\n检查AI列的source_cols是否在column_data中:")
    for config in ai_columns_config:
        target_col = config['target_col']
        source_cols = config['source_cols']
        depends_on = config['depends_on']
        
        print(f"\n{target_col}列:")
        print(f"  source_cols: {source_cols}")
        print(f"  depends_on: {depends_on}")
        
        for source_col in source_cols:
            found = False
            for col_data in column_data:
                col_source_cols = col_data.get('source_cols')
                if col_source_cols == source_col:
                    found = True
                    print(f"\n  源列 {source_col}:")
                    print(f"    col: {col_data.get('col')}")
                    print(f"    head: {col_data.get('head')}")
                    print(f"    source_cols: {col_data.get('source_cols')}")
                    print(f"    data长度: {len(col_data.get('data', []))}")
                    print(f"    前5行数据: {col_data.get('data', [])[:5]}")
                    break
            
            if not found:
                print(f"\n  ❌ 源列 {source_col} 未在column_data中找到")
    
    print("\n" + "=" * 100)
    print("检查完成！")
    print("=" * 100)

if __name__ == "__main__":
    check_column_data_for_ai_columns()
