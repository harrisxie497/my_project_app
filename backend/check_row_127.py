"""
检查原始文件中第127行的第一列A的数据
"""

from openpyxl import load_workbook
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def check_row_127():
    """检查原始文件中第127行的第一列A的数据"""
    print("=" * 100)
    print("检查原始文件中第127行的第一列A的数据")
    print("=" * 100)
    
    original_file_path = "C:\\Users\\harris.xie\\Documents\\trae_projects\\japan\\backend\\storage\\tasks\\t_0fc5b76e\\original.xlsx"
    
    try:
        # 加载工作簿
        workbook = load_workbook(original_file_path)
        sheet = workbook.active
        
        print(f"\n原始文件路径: {original_file_path}")
        print(f"工作表名称: {sheet.title}")
        
        # 读取第127行的数据
        row_127 = []
        for cell in sheet[127]:
            row_127.append(cell.value)
        
        print(f"\n第127行数据: {row_127[:10]}")
        print(f"第127行第一列A的数据: {row_127[0]}")
        
        # 读取第126行和第128行的数据
        row_126 = []
        for cell in sheet[126]:
            row_126.append(cell.value)
        
        row_128 = []
        for cell in sheet[128]:
            row_128.append(cell.value)
        
        print(f"\n第126行数据: {row_126[:10]}")
        print(f"第126行第一列A的数据: {row_126[0]}")
        
        print(f"\n第128行数据: {row_128[:10]}")
        print(f"第128行第一列A的数据: {row_128[0]}")
        
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
    check_row_127()
