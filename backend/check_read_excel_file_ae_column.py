"""
检查read_excel_file方法读取AE列的值
"""

from app.services.excel_reader import read_excel_file
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def check_read_excel_file_ae_column():
    """检查read_excel_file方法读取AE列的值"""
    print("=" * 100)
    print("检查read_excel_file方法读取AE列的值")
    print("=" * 100)
    
    original_file_path = "C:\\Users\\harris.xie\\Documents\\trae_projects\\japan\\backend\\storage\\tasks\\t_e4caaadc\\original.xlsx"
    
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
        
        # 查找AE列的数据
        for col in result['column_data']:
            if col['source_cols'] == 'AE':
                print(f"\nAE列数据:")
                print(f"  列名: {col['source_cols']}")
                print(f"  表头: {col['head']}")
                print(f"  数据行数: {col['len']}")
                print(f"  前10个数据: {col['data'][:10]}")
                print(f"  最后10个数据: {col['data'][-10:]}")
                break
        
        print("\n" + "=" * 100)
        print("检查完成！")
        print("=" * 100)
        
    except Exception as e:
        print(f"\n❌ 检查失败: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    check_read_excel_file_ae_column()
