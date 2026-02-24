"""
检查原始文件中第7行的第一列A的数据
"""

from openpyxl import load_workbook
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def check_row_7():
    """检查原始文件中第7行的第一列A的数据"""
    print("=" * 100)
    print("检查原始文件中第7行的第一列A的数据")
    print("=" * 100)
    
    original_file_path = "C:\\Users\\harris.xie\\Documents\\trae_projects\\japan\\backend\\storage\\tasks\\t_e4caaadc\\original.xlsx"
    
    try:
        # 加载工作簿
        workbook = load_workbook(original_file_path)
        sheet = workbook.active
        
        print(f"\n原始文件路径: {original_file_path}")
        print(f"工作表名称: {sheet.title}")
        
        # 读取第7行的数据
        row_7 = []
        for cell in sheet[7]:
            row_7.append(cell.value)
        
        print(f"\n第7行数据: {row_7[:10]}")
        print(f"第7行第一列A的数据: {row_7[0]}")
        
        # 读取第6行和第8行的数据
        row_6 = []
        for cell in sheet[6]:
            row_6.append(cell.value)
        
        row_8 = []
        for cell in sheet[8]:
            row_8.append(cell.value)
        
        print(f"\n第6行数据: {row_6[:10]}")
        print(f"第6行第一列A的数据: {row_6[0]}")
        
        print(f"\n第8行数据: {row_8[:10]}")
        print(f"第8行第一列A的数据: {row_8[0]}")
        
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
    check_row_7()
