"""
简单的列处理测试 - 只处理前3个列
"""

from app.services.excel_reader import read_excel_file
from app.services.customs_processor import CustomsProcessor
from app.core.database import SessionLocal
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def test_simple():
    """简单的列处理测试"""
    print("=" * 100)
    print("简单的列处理测试")
    print("=" * 100)
    
    # 1. 读取原始Excel文件
    print("\n" + "-" * 100)
    print("步骤1: 读取原始Excel文件")
    print("-" * 100)
    
    file_path = "C:\\Users\\harris.xie\\Documents\\trae_projects\\japan\\backend\\storage\\tasks\\t_2174140b\\original.xlsx"
    
    result = read_excel_file(
        file_path=file_path,
        file_type='CUSTOMS',
        file_role='SOURCE'
    )
    
    print(f"column_data列数: {len(result['column_data'])}")
    print(f"data_row_count: {result.get('data_row_count', 'N/A')}")
    
    # 显示前3列的数据
    print("\n前3列数据:")
    for i, col in enumerate(result['column_data'][:3], start=1):
        print(f"  列{i} - source_cols: {col.get('source_cols')}, head: {col.get('head')}")
    
    # 2. 使用CustomsProcessor处理列
    print("\n" + "-" * 100)
    print("步骤2: 使用CustomsProcessor处理列")
    print("-" * 100)
    
    task_dir = "C:\\Users\\harris.xie\\Documents\\trae_projects\\japan\\backend\\storage\\tasks\\t_2174140b"
    
    db_session = SessionLocal()
    try:
        processor = CustomsProcessor(
            task_dir=task_dir,
            db_session=db_session,
            file_type='CUSTOMS'
        )
        
        # 获取field_pipelines配置
        field_pipelines = processor._get_field_pipelines()
        
        # 只处理前3个列
        field_pipelines = field_pipelines[:3]
        
        print(f"\n处理前3个列:")
        for i, pipeline in enumerate(field_pipelines, start=1):
            print(f"  列{i} - target_col: {pipeline.get('target_col')}, source_cols: {pipeline.get('source_cols')}")
        
        # 处理列数据
        processed_column_data = processor._process_columns(
            column_data=result['column_data'],
            data_row_count=result.get('data_row_count')
        )
        
        print(f"\n处理完成 - 处理列数: {len(processed_column_data)}")
        
        # 显示处理后的列数据
        print("\n处理后的列数据:")
        for i, col in enumerate(processed_column_data, start=1):
            print(f"  列{i} ({col.get('head')}): {col.get('len')} 行")
        
    except Exception as e:
        print(f"\n测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        db_session.close()


if __name__ == "__main__":
    test_simple()
