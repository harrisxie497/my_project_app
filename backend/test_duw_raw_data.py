"""
从excel_reader.py开始，测试D、U、W列的原始数据
"""

from app.services.excel_reader import read_excel_file
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def test_duw_raw_data():
    """从excel_reader.py开始，测试D、U、W列的原始数据"""
    print("=" * 100)
    print("从excel_reader.py开始，测试D、U、W列的原始数据")
    print("=" * 100)
    
    # 1. 读取原始Excel文件
    print("\n" + "-" * 100)
    print("步骤1: 读取原始Excel文件")
    print("-" * 100)
    
    file_path = "C:\\Users\\harris.xie\\Documents\\trae_projects\\japan\\backend\\storage\\tasks\\t_2174140b\\original.xlsx"
    
    result = read_excel_file(
        file_path=file_path,
        file_type='CUSTOMS',
        file_role='SOURCE'
    )
    
    print(f"data_row_count: {result.get('data_row_count', 'N/A')}")
    
    # 2. 显示D、U、W列的原始数据
    print("\n" + "-" * 100)
    print("D、U、W列的原始数据")
    print("-" * 100)
    
    for col in result['column_data']:
        if col.get('source_cols') in ['D', 'U', 'W']:
            print(f"\n列 {col.get('source_cols')} ({col.get('head')}):")
            print(f"  len: {col.get('len')}")
            print(f"  前5条: {col.get('data')[:5]}")
            print(f"  后5条: {col.get('data')[-5:]}")
            print(f"  所有值: {col.get('data')}")


if __name__ == "__main__":
    test_duw_raw_data()
