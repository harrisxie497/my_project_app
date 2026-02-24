"""
测试L列的处理过程 - 检查policy_copy_regex规则
"""

from app.services.excel_reader import read_excel_file
from app.services.customs_processor import CustomsProcessor
from app.core.database import SessionLocal
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def test_l_column_regex():
    """测试L列的处理过程 - 检查policy_copy_regex规则"""
    print("=" * 100)
    print("测试L列的处理过程 - 检查policy_copy_regex规则")
    print("=" * 100)
    
    # 1. 读取Excel文件
    print("\n" + "-" * 100)
    print("步骤1: 读取Excel文件")
    print("-" * 100)
    
    file_path = "C:\\Users\\harris.xie\\Documents\\trae_projects\\japan\\backend\\storage\\tasks\\t_2174140b\\original.xlsx"
    
    result = read_excel_file(
        file_path=file_path,
        file_type='CUSTOMS',
        file_role='SOURCE'
    )
    
    # 2. 查看Q列的数据
    print("\n" + "-" * 100)
    print("步骤2: 查看Q列的数据")
    print("-" * 100)
    
    for col in result.get('column_data', []):
        source_cols = col.get('source_cols')
        if source_cols == 'Q':
            head = col.get('head')
            data = col.get('data')
            print(f"\n列 {source_cols} ({head}):")
            print(f"  len: {col.get('len')}")
            print(f"  前5条: {data[:5]}")
            print(f"  后5条: {data[-5:]}")
            
            # 检查是否匹配regex
            import re
            regex = r'^\d{7}$'
            for idx, value in enumerate(data[:10]):
                if value is not None:
                    value_str = str(value).replace('-', '')
                    match = re.match(regex, value_str)
                    print(f"  第{idx + 1}行: {value} -> {value_str} -> 匹配: {match is not None}")


if __name__ == "__main__":
    test_l_column_regex()
