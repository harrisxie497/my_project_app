"""
检查原始文件和结果文件的列数，并打印每一列的前5个数据
"""

from app.services.excel_reader import read_excel_file
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def test_original_and_result_files():
    """测试原始文件和结果文件"""
    print("=" * 100)
    print("检查原始文件和结果文件")
    print("=" * 100)
    
    original_file_path = "C:\\Users\\harris.xie\\Documents\\trae_projects\\japan\\backend\\storage\\tasks\\t_0fc5b76e\\original.xlsx"
    result_file_path = "C:\\Users\\harris.xie\\Documents\\trae_projects\\japan\\backend\\storage\\tasks\\t_0fc5b76e\\result.xlsx"
    
    # 读取原始文件
    print("\n" + "=" * 100)
    print("读取原始文件")
    print("=" * 100)
    original_result = read_excel_file(
        file_path=original_file_path,
        file_type='CUSTOMS',
        file_role='SOURCE'
    )
    
    print(f"\n原始文件路径: {original_file_path}")
    print(f"总列数: {len(original_result.get('column_data', []))}")
    
    # 打印原始文件每一列的前5个数据
    for col in original_result.get('column_data', []):
        col_name = col.get('head', '')
        col_data = col.get('data', [])
        col_len = len(col_data)
        
        print(f"\n{'=' * 100}")
        print(f"原始文件 - 列: {col_name}")
        print(f"{'=' * 100}")
        print(f"数据行数: {col_len}")
        
        if col_len > 0:
            print(f"前5个数据: {col_data[:5]}")
        else:
            print("前5个数据: []")
    
    # 读取结果文件
    print("\n" + "=" * 100)
    print("读取结果文件")
    print("=" * 100)
    result_result = read_excel_file(
        file_path=result_file_path,
        file_type='CUSTOMS',
        file_role='SOURCE'
    )
    
    print(f"\n结果文件路径: {result_file_path}")
    print(f"总列数: {len(result_result.get('column_data', []))}")
    
    # 打印结果文件每一列的前5个数据
    for col in result_result.get('column_data', []):
        col_name = col.get('head', '')
        col_data = col.get('data', [])
        col_len = len(col_data)
        
        print(f"\n{'=' * 100}")
        print(f"结果文件 - 列: {col_name}")
        print(f"{'=' * 100}")
        print(f"数据行数: {col_len}")
        
        if col_len > 0:
            print(f"前5个数据: {col_data[:5]}")
        else:
            print("前5个数据: []")
    
    # 比较原始文件和结果文件的列数
    print("\n" + "=" * 100)
    print("比较原始文件和结果文件的列数")
    print("=" * 100)
    original_cols = [col.get('head', '') for col in original_result.get('column_data', [])]
    result_cols = [col.get('head', '') for col in result_result.get('column_data', [])]
    
    print(f"\n原始文件列数: {len(original_cols)}")
    print(f"结果文件列数: {len(result_cols)}")
    
    # 找出在结果文件中但不在原始文件中的列
    only_in_result = [col for col in result_cols if col not in original_cols]
    if only_in_result:
        print(f"\n只在结果文件中的列: {only_in_result}")
    
    # 找出在原始文件中但不在结果文件中的列
    only_in_original = [col for col in original_cols if col not in result_cols]
    if only_in_original:
        print(f"只在原始文件中的列: {only_in_original}")
    
    print("\n" + "=" * 100)
    print("测试完成！")
    print("=" * 100)


if __name__ == "__main__":
    test_original_and_result_files()
