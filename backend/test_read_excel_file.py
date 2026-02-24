"""
测试read_excel_file方法的返回结果是否和预期一样
"""

from app.services.excel_reader import read_excel_file
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def test_read_excel_file():
    """测试read_excel_file方法的返回结果是否和预期一样"""
    print("=" * 100)
    print("测试read_excel_file方法的返回结果是否和预期一样")
    print("=" * 100)
    
    original_file_path = "C:\\Users\\harris.xie\\Documents\\trae_projects\\japan\\backend\\storage\\tasks\\t_0fc5b76e\\original.xlsx"
    
    try:
        # 调用read_excel_file方法
        result = read_excel_file(
            original_file_path,
            file_type='CUSTOMS',
            file_role='SOURCE'
        )
        
        # 打印返回结果
        print(f"\n返回结果:")
        print(f"  第一行长度: {len(result['first_row'])}")
        print(f"  第一行数据（前10个）: {result['first_row'][:10]}")
        print(f"  列数据数量: {len(result['column_data'])}")
        print(f"  数据行数: {result['data_row_count']}")
        
        # 打印每一列的数据
        print(f"\n每一列的数据:")
        for col in result['column_data']:
            source_cols = col.get('source_cols')
            head = col.get('head')
            data = col.get('data')
            data_len = col.get('len')
            
            print(f"\n  列名: {source_cols}, 表头: {head}, 数据行数: {data_len}")
            if data_len > 0:
                print(f"    前5个数据: {data[:5]}")
                print(f"    最后5个数据: {data[-5:]}")
        
        print("\n" + "=" * 100)
        print("测试完成！")
        print("=" * 100)
        
    except Exception as e:
        print(f"\n❌ 测试失败: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    test_read_excel_file()
