"""
测试B、D、R列的CALC计算情况 - 使用新的process_field_v2方法
"""

from app.services.excel_reader import read_excel_file
from app.services.field_handlers_v2 import process_field_v2
from app.core.database import SessionLocal
import logging

logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def test_bdr_calc_v2():
    """测试B、D、R列的CALC计算情况 - 使用新的process_field_v2方法"""
    print("=" * 100)
    print("测试B、D、R列的CALC计算情况 - 使用新的process_field_v2方法")
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
    
    # 2. 获取field_pipelines配置
    print("\n" + "-" * 100)
    print("步骤2: 获取field_pipelines配置")
    print("-" * 100)
    
    db_session = SessionLocal()
    try:
        from app.services.customs_processor import CustomsProcessor
        task_dir = "C:\\Users\\harris.xie\\Documents\\trae_projects\\japan\\backend\\storage\\tasks\\t_2174140b"
        
        processor = CustomsProcessor(
            task_dir=task_dir,
            db_session=db_session,
            file_type='CUSTOMS'
        )
        
        field_pipelines = processor._get_field_pipelines()
        
        # 只处理B、D、R列
        bdr_pipelines = [p for p in field_pipelines if p.get('target_col') in ['B', 'D', 'R']]
        
        print(f"\nB、D、R列的配置:")
        for pipeline in bdr_pipelines:
            print(f"\n列 {pipeline.get('target_col')} ({pipeline.get('target_header')}):")
            print(f"  map_op: {pipeline.get('map_op')}")
            print(f"  source_cols: {pipeline.get('source_cols')}")
            print(f"  field_type: {pipeline.get('field_type')}")
            print(f"  rule_ref: {pipeline.get('rule_ref')}")
            print(f"  depends_on: {pipeline.get('depends_on')}")
            print(f"  rule_params_json: {pipeline.get('rule_params_json')}")
        
        # 3. 处理列数据
        print("\n" + "-" * 100)
        print("步骤3: 处理列数据")
        print("-" * 100)
        
        # 构建列数据映射
        column_data_map = {}
        for col in result['column_data']:
            col_source_cols = col.get('source_cols')
            if col_source_cols:
                column_data_map[col_source_cols] = col.get('data')
        
        # 处理B、D、R列
        processed_column_data = {}
        for pipeline in bdr_pipelines:
            target_col = pipeline.get('target_col')
            target_header = pipeline.get('target_header')
            map_op = pipeline.get('map_op')
            source_cols = pipeline.get('source_cols')
            field_type = pipeline.get('field_type')
            rule_ref = pipeline.get('rule_ref')
            depends_on = pipeline.get('depends_on')
            
            print(f"\n处理列 {target_col} ({target_header}):")
            
            processed_values = []
            
            # 处理每一行
            for row_idx in range(result.get('data_row_count')):
                # 构建row字典
                row = {}
                
                # 添加源列的值
                if source_cols:
                    for col in source_cols:
                        if col in column_data_map:
                            row[col] = column_data_map[col][row_idx]
                
                # 添加依赖列的值
                if depends_on:
                    for dep_col in depends_on:
                        if dep_col in column_data_map:
                            row[dep_col] = column_data_map[dep_col][row_idx]
                
                # 添加行索引
                row['_row_index'] = row_idx
                
                # 处理字段
                try:
                    processed_value = process_field_v2(
                        map_op, source_cols, field_type, rule_ref, row, pipeline, None, None
                    )
                    processed_values.append(processed_value)
                except Exception as e:
                    print(f"  处理第{row_idx + 1}行失败: {str(e)}")
                    processed_values.append(None)
            
            processed_column_data[target_col] = {
                'target_col': target_col,
                'head': target_header,
                'data': processed_values,
                'len': len(processed_values)
            }
        
        # 4. 显示处理结果
        print("\n" + "-" * 100)
        print("处理后的列数据（B、D、R列）")
        print("-" * 100)
        
        for target_col in ['B', 'D', 'R']:
            if target_col in processed_column_data:
                col = processed_column_data[target_col]
                print(f"\n列 {col.get('target_col')} ({col.get('head')}):")
                print(f"  len: {col.get('len')}")
                print(f"  前5条: {col.get('data')[:5]}")
                print(f"  后5条: {col.get('data')[-5:]}")
                
                # 验证B列
                if target_col == 'B':
                    expected = list(range(1, result.get('data_row_count') + 1))
                    actual = col.get('data')
                    if actual == expected:
                        print(f"  ✓ B列是正确的序号序列（1到{result.get('data_row_count')}）")
                    else:
                        print(f"  ✗ B列序号序列不正确")
                        print(f"    期望: {expected[:5]}...{expected[-5:]}")
                        print(f"    实际: {actual[:5]}...{actual[-5:]}")
                
                # 验证D列
                if target_col == 'D':
                    # D列应该复制C列的数据
                    c_col_data = column_data_map.get('C', [])
                    expected = c_col_data
                    actual = col.get('data')
                    if actual == expected:
                        print(f"  ✓ D列正确复制了C列的数据")
                    else:
                        print(f"  ✗ D列没有正确复制C列的数据")
                        print(f"    C列前5条: {expected[:5]}")
                        print(f"    D列前5条: {actual[:5]}")
        
    except Exception as e:
        print(f"\n测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        db_session.close()


if __name__ == "__main__":
    test_bdr_calc_v2()
