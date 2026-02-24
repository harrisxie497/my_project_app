"""
测试D、U、W列的处理结果 - 简单版本
"""

from app.services.excel_reader import read_excel_file
from app.services.customs_processor import CustomsProcessor
from app.core.database import SessionLocal
import logging

logging.basicConfig(level=logging.WARNING, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def test_duw_simple():
    """测试D、U、W列的处理结果 - 简单版本"""
    print("=" * 100)
    print("测试D、U、W列的处理结果 - 简单版本")
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
    
    print(f"data_row_count: {result.get('data_row_count', 'N/A')}")
    
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
        
        # 只处理D、U、W列
        duw_pipelines = [p for p in field_pipelines if p.get('target_col') in ['D', 'U', 'W']]
        
        print(f"\nD、U、W列的配置:")
        for pipeline in duw_pipelines:
            print(f"\n列 {pipeline.get('target_col')} ({pipeline.get('target_header')}):")
            print(f"  map_op: {pipeline.get('map_op')}")
            print(f"  source_cols: {pipeline.get('source_cols')}")
            print(f"  field_type: {pipeline.get('field_type')}")
            print(f"  rule_ref: {pipeline.get('rule_ref')}")
            print(f"  depends_on: {pipeline.get('depends_on')}")
        
        # 处理列数据
        processed_column_data = processor._process_columns(
            column_data=result['column_data'],
            data_row_count=result.get('data_row_count')
        )
        
        # 只显示D、U、W列的处理结果
        print("\n" + "-" * 100)
        print("处理后的列数据（D、U、W列）")
        print("-" * 100)
        
        for col in processed_column_data:
            if col.get('target_col') in ['D', 'U', 'W']:
                print(f"\n列 {col.get('target_col')} ({col.get('head')}):")
                print(f"  len: {col.get('len')}")
                print(f"  前5条: {col.get('data')[:5]}")
                print(f"  后5条: {col.get('data')[-5:]}")
        
    except Exception as e:
        print(f"\n测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        db_session.close()


if __name__ == "__main__":
    test_duw_simple()
