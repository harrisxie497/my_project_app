"""
调试read_excel_file函数中的sheet_name参数
"""

from app.services.excel_reader import read_excel_file
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def debug_read_excel_file():
    """调试read_excel_file函数中的sheet_name参数"""
    print("=" * 100)
    print("调试read_excel_file函数中的sheet_name参数")
    print("=" * 100)
    
    # 原始文件路径
    original_file_path = r'C:\Users\harris.xie\Documents\trae_projects\japan\backend\storage\tasks\t_aa9d170a\original.xlsx'
    
    # 文件类型
    file_type = 'CUSTOMS'
    
    # 读取Excel文件
    print(f"\n读取Excel文件...")
    print(f"  file_path: {original_file_path}")
    print(f"  file_type: {file_type}")
    print(f"  file_role: SOURCE")
    print(f"  sheet_name: None")
    
    try:
        result = read_excel_file(
            original_file_path,
            sheet_name=None,
            file_type=file_type,
            file_role='SOURCE'
        )
        
        print(f"\n✅ 读取成功！")
        print(f"  工作表名称: {result['worksheet'].title}")
        print(f"  数据行数: {result['data_row_count']}")
        print(f"  列数: {len(result['column_data'])}")
        
    except Exception as e:
        print(f"\n❌ 读取失败！")
        print(f"  错误: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 100)
    print("调试完成！")
    print("=" * 100)

if __name__ == "__main__":
    debug_read_excel_file()
