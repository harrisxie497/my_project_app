"""
检查结果文件的第一行是否正确
"""

from openpyxl import load_workbook
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def check_result_file_first_row():
    """检查结果文件的第一行是否正确"""
    print("=" * 100)
    print("检查结果文件的第一行是否正确")
    print("=" * 100)
    
    result_file_path = "C:\\Users\\harris.xie\\Documents\\trae_projects\\japan\\backend\\storage\\tasks\\t_0fc5b76e\\result.xlsx"
    
    try:
        # 加载工作簿
        workbook = load_workbook(result_file_path)
        sheet = workbook.active
        
        print(f"\n结果文件路径: {result_file_path}")
        print(f"工作表名称: {sheet.title}")
        
        # 读取第一行（特殊第一行）
        first_row = []
        for cell in sheet[1]:
            first_row.append(cell.value)
        
        print(f"\n第一行数据: {first_row}")
        
        # 读取表头行
        header_row = []
        for cell in sheet[2]:
            header_row.append(cell.value)
        
        print(f"\n表头行数据: {header_row}")
        
        # 读取第一行数据
        data_row = []
        for cell in sheet[3]:
            data_row.append(cell.value)
        
        print(f"\n第一行数据: {data_row}")
        
        # 关闭工作簿
        workbook.close()
        
        print("\n" + "=" * 100)
        print("检查完成！")
        print("=" * 100)
        
    except Exception as e:
        print(f"\n❌ 检查失败: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    check_result_file_first_row()
