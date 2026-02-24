"""
逐列测试数据，看看D列的无限循环问题是否修复
"""

from app.services.excel_reader import read_excel_file
from app.services.customs_processor import CustomsProcessor
from app.core.database import SessionLocal
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def test_columns_one_by_one():
    """逐列测试数据"""
    print("=" * 100)
    print("逐列测试数据")
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
            
            # 只测试前10列
            if target_col in ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K']:
                print(f"  order_num: {pipeline.get('order_num')}")
                print(f"  map_op: {pipeline.get('map_op')}")
                print(f"  source_cols: {pipeline.get('source_cols')}")
                print(f"  field_type: {pipeline.get('field_type')}")
                print(f"  rule_ref: {pipeline.get('rule_ref')}")
                print(f"  depends_on: {pipeline.get('depends_on')}")
                print(f"  rule_params_json:")
                rule_params_json = pipeline.get('rule_params_json', {})
                for key, value in rule_params_json.items():
                    print(f"    {key}: {value}")
                
                # 测试处理
                try:
                    # 获取源列数据
                    source_cols = pipeline.get('source_cols', [])
                    source_data = {}
                    for col in source_cols:
                        if col in processor.processed_column_data_map:
                            source_data[col] = processor.processed_column_data_map[col]
                    
                    # 模拟一行数据
                    row = {'_row_index': 0}
                    row.update(source_data)
                    
                    # 处理字段
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
                    
                except Exception as e:
                    print(f"  ❌ 测试失败: {str(e)}")
                    import traceback
                    traceback.print_exc()
                
                print(f"{'=' * 100}")
        
    except Exception as e:
        print(f"\n❌ 测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        db_session.close()


if __name__ == "__main__":
    test_columns_one_by_one()
