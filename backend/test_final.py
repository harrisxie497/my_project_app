"""
最终测试 - 检查所有列的处理结果
"""

from app.services.excel_reader import read_excel_file
from app.services.customs_processor import CustomsProcessor
from app.core.database import SessionLocal
import logging

logging.basicConfig(level=logging.WARNING, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def test_final():
    """最终测试 - 检查所有列的处理结果"""
    print("=" * 100)
    print("最终测试 - 检查所有列的处理结果")
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
        
        # 处理列数据
        processed_column_data = processor._process_columns(
            column_data=result['column_data'],
            data_row_count=result.get('data_row_count')
        )
        
        # 3. 查看所有列的处理结果
        print("\n" + "-" * 100)
        print("步骤3: 查看所有列的处理结果")
        print("-" * 100)
        
        # 按order_num排序
        processed_column_data_sorted = sorted(processed_column_data, key=lambda x: x.get('order_num', 999))
        
        for col in processed_column_data_sorted:
            target_col = col.get('target_col')
            head = col.get('head')
            data = col.get('data')
            order_num = col.get('order_num', 999)
            
            print(f"\n列 {target_col} ({head}) - order_num: {order_num}:")
            print(f"  len: {col.get('len')}")
            print(f"  前3条: {data[:3]}")
            print(f"  后3条: {data[-3:]}")
            
            # 检查是否有None值
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
    test_final()
