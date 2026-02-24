"""
检查C列的值是否为空
"""

from app.services.excel_reader import read_excel_file
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def test_c_column_values():
    """检查C列的值是否为空"""
    print("=" * 100)
    print("检查C列的值是否为空")
    print("=" * 100)
    
    file_path = "C:\\Users\\harris.xie\\Documents\\trae_projects\\japan\\backend\\storage\\tasks\\t_795eb06d\\original.xlsx"
    
    try:
        result = read_excel_file(
            file_path=file_path,
            file_type='CUSTOMS',
            file_role='SOURCE'
        )
        
        # 查找C列的数据
        for col in result.get('column_data', []):
            source_cols = col.get('source_cols')
            if source_cols == 'C':
                data = col.get('data', [])
                print(f"\n列 {source_cols}的数据:")
                print(f"  len: {len(data)}")
                print(f"  前10条: {data[:10]}")
                print(f"  后10条: {data[-10:]}")
                print(f"  是否有空值: {any(v is None or (isinstance(v, str) and v.strip() == '') for v in data)}")
        
    except Exception as e:
        print(f"\n测试失败: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    test_c_column_values()
