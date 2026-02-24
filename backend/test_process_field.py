"""
测试_process_field方法
"""

from app.services.excel_reader import read_excel_file
from app.services.customs_processor import CustomsProcessor
from app.core.database import SessionLocal
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def test_process_field():
    """测试_process_field方法"""
    print("=" * 100)
    print("测试_process_field方法")
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
        
        # 按order_num排序
        field_pipelines_sorted = sorted(field_pipelines, key=lambda x: x.get('order_num', 999))
        
        # 只处理B列和L列
        bl_pipelines = [p for p in field_pipelines_sorted if p.get('target_col') in ['B', 'L']]
        
        print(f"\nB列和L列的配置:")
        for pipeline in bl_pipelines:
            print(f"\n列 {pipeline.get('target_col')} ({pipeline.get('target_header')}):")
            print(f"  order_num: {pipeline.get('order_num')}")
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
        
        # 3. 查看处理后的B列和L列数据
        print("\n" + "-" * 100)
        print("步骤3: 查看处理后的B列和L列数据")
        print("-" * 100)
        
        for col in processed_column_data:
            target_col = col.get('target_col')
            if target_col in ['B', 'L', 'Q']:
                head = col.get('head')
                data = col.get('data')
                print(f"\n列 {target_col} ({head}):")
                print(f"  len: {col.get('len')}")
                print(f"  前5条: {data[:5]}")
                print(f"  后5条: {data[-5:]}")
        
    except Exception as e:
        print(f"\n测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        db_session.close()


if __name__ == "__main__":
    test_process_field()
