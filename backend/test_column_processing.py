"""
测试列处理功能

测试目标：
1. 读取file_definitions表中CUSTOMS OUTPUT的配置
2. 获取field_pipelines配置
3. 依据field_pipelines处理每一列
4. 输出处理后的列数据
"""

from app.services.excel_reader import read_excel_file
from app.services.customs_processor import CustomsProcessor
from app.core.database import SessionLocal
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def test_column_processing():
    """
    测试列处理功能
    
    流程：
    1. 读取原始Excel文件
    2. 获取file_definitions配置（CUSTOMS OUTPUT）
    3. 获取field_pipelines配置
    4. 依据field_pipelines处理每一列
    5. 输出处理后的列数据
    """
    print("=" * 100)
    print("测试列处理功能")
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
    
    print(f"worksheet: {result['worksheet'].title}")
    print(f"first_row长度: {len(result['first_row'])}")
    print(f"column_data列数: {len(result['column_data'])}")
    print(f"data_row_count: {result.get('data_row_count', 'N/A')}")
    
    # 显示前5列的数据
    print("\n前5列数据:")
    for i, col in enumerate(result['column_data'][:5], start=1):
        print(f"  列{i} ({col.get('source_cols')} - {col.get('head')}): {col.get('len')} 行")
        print(f"    前3条数据: {col.get('data')[:3]}")
    
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
        
        print(f"\n处理完成 - 处理列数: {len(processed_column_data)}")
        
        # 显示处理后的列数据
        print("\n" + "-" * 100)
        print("处理后的列数据")
        print("-" * 100)
        
        for i, col in enumerate(processed_column_data[:10], start=1):
            print(f"  列{i} ({col.get('head')}): {col.get('len')} 行")
            print(f"    前3条数据: {col.get('data')[:3]}")
        
        if len(processed_column_data) > 10:
            print(f"  ... 还有 {len(processed_column_data) - 10} 列未显示")
        
        # 验证数据一致性
        print("\n" + "-" * 100)
        print("数据一致性验证")
        print("-" * 100)
        
        data_row_count = result.get('data_row_count', 0)
        all_match = True
        
        for i, col in enumerate(processed_column_data, start=1):
            col_len = col.get('len', 0)
            match = col_len == data_row_count
            all_match = all_match and match
            
            status = "✓" if match else "✗"
            print(f"  {status} 列{i} ({col.get('head')}): {col_len} 行")
        
        print("\n" + "-" * 100)
        if all_match:
            print("✓ 所有列的数据行数一致，测试通过！")
        else:
            print("✗ 存在列数据行数不一致，测试失败！")
        print("-" * 100)
        
        return all_match
        
    except Exception as e:
        print(f"\n✗ 测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        db_session.close()


def test_field_pipelines():
    """
    测试获取field_pipelines配置
    """
    print("\n" + "=" * 100)
    print("测试获取field_pipelines配置")
    print("=" * 100)
    
    task_dir = "C:\\Users\\harris.xie\\Documents\\trae_projects\\japan\\backend\\storage\\tasks\\t_2174140b"
    
    db_session = SessionLocal()
    try:
        processor = CustomsProcessor(
            task_dir=task_dir,
            db_session=db_session,
            file_type='CUSTOMS'
        )
        
        field_pipelines = processor._get_field_pipelines()
        
        # 只处理前5个列，避免输出过多
        field_pipelines = field_pipelines[:5]
        
        print(f"\n获取到 {len(field_pipelines)} 个字段处理配置（仅显示前5个）")
        
        for i, pipeline in enumerate(field_pipelines[:10], start=1):
            print(f"\n配置{i}:")
            print(f"  target_col: {pipeline.get('target_col')}")
            print(f"  target_header: {pipeline.get('target_header')}")
            print(f"  map_op: {pipeline.get('map_op')}")
            print(f"  source_cols: {pipeline.get('source_cols')}")
            print(f"  field_type: {pipeline.get('field_type')}")
            print(f"  rule_ref: {pipeline.get('rule_ref')}")
            print(f"  depends_on: {pipeline.get('depends_on')}")
            print(f"  order: {pipeline.get('order')}")
        
        if len(field_pipelines) > 10:
            print(f"\n... 还有 {len(field_pipelines) - 10} 个配置未显示")
        
    except Exception as e:
        print(f"\n✗ 测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        db_session.close()


def run_all_tests():
    """
    运行所有测试用例
    """
    print("\n" + "=" * 100)
    print("开始运行列处理测试")
    print("=" * 100)
    
    # 测试获取field_pipelines配置
    test_field_pipelines()
    
    # 测试列处理功能
    result = test_column_processing()
    
    print("\n" + "=" * 100)
    print("测试完成")
    print("=" * 100)
    
    return result


if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)
