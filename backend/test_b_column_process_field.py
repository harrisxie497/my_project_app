"""
测试B列的处理过程 - 检查_process_field方法
"""

from app.services.excel_reader import read_excel_file
from app.services.customs_processor import CustomsProcessor
from app.core.database import SessionLocal
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def test_b_column_process_field():
    """测试B列的处理过程 - 检查_process_field方法"""
    print("=" * 100)
    print("测试B列的处理过程 - 检查_process_field方法")
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
        
        # 只处理B列
        b_pipeline = next((p for p in field_pipelines_sorted if p.get('target_col') == 'B'), None)
        
        if b_pipeline:
            print(f"\nB列的配置:")
            print(f"  order_num: {b_pipeline.get('order_num')}")
            print(f"  map_op: {b_pipeline.get('map_op')}")
            print(f"  source_cols: {b_pipeline.get('source_cols')}")
            print(f"  field_type: {b_pipeline.get('field_type')}")
            print(f"  rule_ref: {b_pipeline.get('rule_ref')}")
            print(f"  depends_on: {b_pipeline.get('depends_on')}")
            
            # 测试_process_field方法
            for row_idx in range(5):
                row = {'_row_index': row_idx}
                result = processor._process_field(
                    b_pipeline.get('map_op'),
                    b_pipeline.get('source_cols'),
                    b_pipeline.get('field_type'),
                    b_pipeline.get('rule_ref'),
                    row,
                    None,
                    b_pipeline,
                    None
                )
                print(f"  行号: {row_idx + 1}, 结果: {result}")
        
    except Exception as e:
        print(f"\n测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        db_session.close()


if __name__ == "__main__":
    test_b_column_process_field()
