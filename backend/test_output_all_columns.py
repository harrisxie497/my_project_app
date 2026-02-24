"""
从excel_read.py开始，输出每一列的数据
"""

from app.services.excel_reader import read_excel_file
from app.services.customs_processor import CustomsProcessor
from app.core.database import SessionLocal
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def test_output_all_columns():
    """从excel_read.py开始，输出每一列的数据"""
    print("=" * 100)
    print("从excel_read.py开始，输出每一列的数据")
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
    print(f"column_count: {len(result.get('column_data', []))}")
    
    # 2. 显示原始列数据
    print("\n" + "-" * 100)
    print("步骤2: 显示原始列数据")
    print("-" * 100)
    
    for col in result.get('column_data', []):
        source_cols = col.get('source_cols')
        head = col.get('head')
        data = col.get('data')
        
        print(f"\n列 {source_cols} ({head}):")
        print(f"  len: {col.get('len')}")
        print(f"  前3条: {data[:3]}")
        print(f"  后3条: {data[-3:]}")
    
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
        
        # 获取field_pipelines配置
        field_pipelines = processor._get_field_pipelines()
        
        # 按order_num排序
        field_pipelines_sorted = sorted(field_pipelines, key=lambda x: x.get('order_num', 999))
        
        print(f"\n获取到 {len(field_pipelines_sorted)} 个字段处理配置")
        print(f"按order_num排序后的配置:")
        for pipeline in field_pipelines_sorted:
            print(f"  {pipeline.get('order_num', 999):3d} - 列 {pipeline.get('target_col')} ({pipeline.get('target_header')}) - {pipeline.get('map_op')} - {pipeline.get('field_type')} - {pipeline.get('rule_ref')}")
        
        # 处理列数据
        print("\n" + "-" * 100)
        print("步骤4: 处理列数据（按order_num顺序）")
        print("-" * 100)
        
        processed_column_data = processor._process_columns(
            column_data=result['column_data'],
            data_row_count=result.get('data_row_count')
        )
        
        # 4. 输出每一列的数据
        print("\n" + "-" * 100)
        print("步骤5: 输出每一列的数据")
        print("-" * 100)
        
        # 按order_num排序输出
        processed_column_data_sorted = sorted(processed_column_data, key=lambda x: x.get('order_num', 999))
        
        for col in processed_column_data_sorted:
            target_col = col.get('target_col')
            head = col.get('head')
            data = col.get('data')
            order_num = col.get('order_num', 999)
            
            print(f"\n{'=' * 100}")
            print(f"列 {target_col} ({head}) - order_num: {order_num}")
            print(f"{'=' * 100}")
            print(f"  len: {col.get('len')}")
            print(f"  前3条: {data[:3]}")
            print(f"  后3条: {data[-3:]}")
            
            # 显示非None的数据
            non_none_count = sum(1 for v in data if v is not None and v != '')
            print(f"  非空数据: {non_none_count}/{len(data)}")
        
        print("\n" + "=" * 100)
        print("处理完成")
        print("=" * 100)
        
    except Exception as e:
        print(f"\n测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        db_session.close()


if __name__ == "__main__":
    test_output_all_columns()
