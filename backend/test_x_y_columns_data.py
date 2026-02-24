"""
检查X列和Y列的数据
"""

from app.services.excel_reader import read_excel_file
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def test_x_y_columns_data():
    """检查X列和Y列的数据"""
    print("=" * 100)
    print("检查X列和Y列的数据")
    print("=" * 100)
    
    file_path = "C:\\Users\\harris.xie\\Documents\\trae_projects\\japan\\backend\\storage\\tasks\\t_2174140b\\original.xlsx"
    
    result = read_excel_file(
        file_path=file_path,
        file_type='CUSTOMS',
        file_role='SOURCE'
    )
    
    print(f"data_row_count: {result.get('data_row_count', 'N/A')}")
    
    for col in result.get('column_data', []):
        source_cols = col.get('source_cols')
        if source_cols in ['X', 'Y']:
            head = col.get('head')
            data = col.get('data')
            print(f"\n列 {source_cols} ({head}):")
            print(f"  len: {col.get('len')}")
            print(f"  前5条: {data[:5]}")
            print(f"  后5条: {data[-5:]}")


if __name__ == "__main__":
    test_x_y_columns_data()
