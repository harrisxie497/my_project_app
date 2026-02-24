"""
测试A、B、C、D四列的处理结果 - 详细版本
"""

from app.services.excel_reader import read_excel_file
from app.services.customs_processor import CustomsProcessor
from app.core.database import SessionLocal
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def test_abcd_columns_detailed():
    """测试A、B、C、D四列的处理结果 - 详细版本"""
    print("=" * 100)
    print("测试A、B、C、D四列的处理结果 - 详细版本")
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
        
        # 只处理A、B、C、D列
        abcd_pipelines = [p for p in field_pipelines if p.get('target_col') in ['A', 'B', 'C', 'D']]
        
        print(f"\nA、B、C、D列的配置:")
        for pipeline in abcd_pipelines:
            print(f"  列{pipeline.get('target_col')} - map_op: {pipeline.get('map_op')}, source_cols: {pipeline.get('source_cols')}, field_type: {pipeline.get('field_type')}")
        
        # 处理列数据
        processed_column_data = processor._process_columns(
            column_data=result['column_data'],
            data_row_count=result.get('data_row_count')
        )
        
        # 只显示A、B、C、D列的处理结果
        print("\n" + "-" * 100)
        print("处理后的列数据（A、B、C、D列）")
        print("-" * 100)
        
        for col in processed_column_data:
            if col.get('head') in ['会员编号', '序号', 'HAWB番号', '現地問合せ番号']:
                print(f"\n列 {col.get('head')}:")
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
    test_abcd_columns_detailed()
