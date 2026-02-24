"""
测试D列的复制问题
"""

from app.services.excel_reader import read_excel_file
from app.services.customs_processor import CustomsProcessor
from app.core.database import SessionLocal
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def test_d_column_copy():
    """测试D列的复制问题"""
    print("=" * 100)
    print("测试D列的复制问题")
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
    
    # 2. 查看C列和D列的原始数据
    print("\n" + "-" * 100)
    print("步骤2: 查看C列和D列的原始数据")
    print("-" * 100)
    
    for col in result.get('column_data', []):
        source_cols = col.get('source_cols')
        if source_cols in ['C', 'D']:
            head = col.get('head')
            data = col.get('data')
            print(f"\n列 {source_cols} ({head}):")
            print(f"  len: {col.get('len')}")
            print(f"  前5条: {data[:5]}")
            print(f"  后5条: {data[-5:]}")
    
    # 3. 使用CustomsProcessor处理列
    print("\n" + "-" * 100)
    print("步骤3: 使用CustomsProcessor处理列")
    print("-" * 100)
    
    task_dir = "C:\\Users\\harris.xie\\Documents\\trae_projects\\japan\\backend\\storage\\tasks\\t_2174140b"
    
    db_session = SessionLocal()
    try:
        processor = CustomsProcessor(
            task_dir=task_dir,
            db_session=db_session,
            file_type='CUSTOMS'
        )
        
        # 获取D列的配置
        field_pipelines = processor._get_field_pipelines()
        d_pipeline = next((p for p in field_pipelines if p.get('target_col') == 'D'), None)
        
        if d_pipeline:
            print(f"\nD列的配置:")
            print(f"  map_op: {d_pipeline.get('map_op')}")
            print(f"  source_cols: {d_pipeline.get('source_cols')}")
            print(f"  field_type: {d_pipeline.get('field_type')}")
            print(f"  rule_ref: {d_pipeline.get('rule_ref')}")
            print(f"  depends_on: {d_pipeline.get('depends_on')}")
            print(f"  rule_params_json: {d_pipeline.get('rule_params_json')}")
        
        # 处理列数据
        processed_column_data = processor._process_columns(
            column_data=result['column_data'],
            data_row_count=result.get('data_row_count')
        )
        
        # 4. 查看处理后的D列数据
        print("\n" + "-" * 100)
        print("步骤4: 查看处理后的D列数据")
        print("-" * 100)
        
        for col in processed_column_data:
            target_col = col.get('target_col')
            if target_col in ['C', 'D']:
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
    test_d_column_copy()
