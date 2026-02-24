"""
测试后端任务运行，看看每一列处理的数据量是多少，以及有没有不符合预期的数据处理
"""

from app.services.excel_reader import read_excel_file
from app.services.customs_processor import CustomsProcessor
from app.core.database import SessionLocal
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def test_task_processing():
    """测试后端任务运行"""
    print("=" * 100)
    print("测试后端任务运行")
    print("=" * 100)
    
    task_dir = "C:\\Users\\harris.xie\\Documents\\trae_projects\\japan\\backend\\storage\\tasks\\t_795eb06d"
    
    db_session = SessionLocal()
    try:
        processor = CustomsProcessor(
            task_dir=task_dir,
            db_session=db_session,
            file_type='CUSTOMS'
        )
        
        # 获取字段处理配置
        field_pipelines = processor._get_field_pipelines()
        
        # 按order_num排序
        field_pipelines_sorted = sorted(field_pipelines, key=lambda x: x.get('order_num', 999))
        
        # 逐列测试
        for pipeline in field_pipelines_sorted:
            target_col = pipeline.get('target_col')
            print(f"\n{'=' * 100}")
            print(f"测试列: {target_col}")
            print(f"{'=' * 100}")
            
            # 获取源列数据
            source_cols = pipeline.get('source_cols', [])
            source_data = {}
            for col in source_cols:
                if col in processor.processed_column_data_map:
                    source_data[col] = processor.processed_column_data_map[col]
            
            # 模拟一行数据
            row = {'_row_index': 0}
            row.update(source_data)
            
            # 测试处理
            try:
                processed_value = processor._process_field(
                    map_op=pipeline.get('map_op'),
                    source_cols=pipeline.get('source_cols', []),
                    field_type=pipeline.get('field_type'),
                    rule_ref=pipeline.get('rule_ref', []),
                    row=row,
                    pipeline=pipeline
                )
                
                print(f"  输入值: {row.get(target_col)}")
                print(f"  输出值: {processed_value}")
                
                # 检查是否为None
                if processed_value is None:
                    print(f"  ⚠️ 输出值为None！")
                
                # 检查是否为空字符串
                if isinstance(processed_value, str) and processed_value.strip() == '':
                    print(f"  ⚠️ 输出值为空字符串！")
                
                # 检查是否与输入值相同
                if processed_value == row.get(target_col):
                    print(f"  ℹ️ 输出值与输入值相同")
                
                # 检查是否为数字
                if isinstance(processed_value, (int, float)):
                    print(f"  ℹ️ 输出值为数字")
                
                # 检查是否为布尔值
                if isinstance(processed_value, bool):
                    print(f"  ℹ️ 输出值为布尔值")
                
            except Exception as e:
                print(f"  ❌ 测试失败: {str(e)}")
                import traceback
                traceback.print_exc()
        
        print(f"\n{'=' * 100}")
        print("测试完成！")
        
    except Exception as e:
        print(f"\n❌ 测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        db_session.close()


if __name__ == "__main__":
    test_task_processing()
