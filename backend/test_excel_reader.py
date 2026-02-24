from app.services.excel_reader import read_excel_file
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def test_read_excel():
    """测试read_excel_file函数"""
    print("=" * 100)
    print("测试read_excel_file函数")
    print("=" * 100)
    
    # 测试读取CUSTOMS SOURCE文件
    file_path = "C:\\Users\\harris.xie\\Documents\\trae_projects\\japan\\backend\\storage\\tasks\\t_2174140b\\original.xlsx"
    
    try:
        print(f"\n开始读取文件: {file_path}")
        print(f"文件类型: CUSTOMS, 文件角色: SOURCE")
        print(f"期望的表头行: 第2行")
        print(f"期望的数据开始行: 第3行")
        print(f"期望的列数: 41")
        print()
        
        result = read_excel_file(
            file_path=file_path,
            file_type='CUSTOMS',
            file_role='SOURCE'
        )
        
        print("\n" + "=" * 100)
        print("读取结果")
        print("=" * 100)
        print(f"worksheet: {result['worksheet'].title}")
        print(f"first_row长度: {len(result['first_row'])}")
        print(f"first_row内容: {result['first_row']}")
        print(f"column_data列数: {len(result['column_data'])}")
        print(f"data_row_count: {result.get('data_row_count', 'N/A')}")
        
        print("\n" + "-" * 100)
        print("列数据详情")
        print("-" * 100)
        for i, col in enumerate(result['column_data'][:10], start=1):  # 只打印前10列
            print(f"  列{i}:")
            print(f"    source_cols: {col.get('source_cols')}")
            print(f"    head: {col.get('head')}")
            print(f"    len: {col.get('len')}")
            if col.get('len') <= 5:
                print(f"    data: {col.get('data')}")
            else:
                print(f"    data: {col.get('data')[:5]} ... (共{col.get('len')}项)")
        
        if len(result['column_data']) > 10:
            print(f"  ... 还有 {len(result['column_data']) - 10} 列未显示")
        
        print("\n" + "=" * 100)
        print("测试完成")
        print("=" * 100)
        
    except Exception as e:
        print("\n" + "=" * 100)
        print("测试失败")
        print("=" * 100)
        print(f"错误: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_read_excel()
