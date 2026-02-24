"""
测试A、B、C、D四列的处理结果

预期结果：
1. A列 - 固定值：head="会员编号", data=["DIDA","DIDA"...]（124个固定值）
2. B列 - 序号：head="序号", data=[1,2,3,...]（从1开始的序号，124个）
3. C列 - COPY操作：从源列复制
4. D列 - COPY操作：从源列复制
"""

from app.services.excel_reader import read_excel_file
from app.services.customs_processor import CustomsProcessor
from app.core.database import SessionLocal
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def test_abcd_columns():
    """测试A、B、C、D四列的处理结果"""
    print("=" * 100)
    print("测试A、B、C、D四列的处理结果")
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
    
    # 显示A、B、C、D列的原始数据
    print("\n原始数据（A、B、C、D列）:")
    for col in result['column_data']:
        if col.get('source_cols') in ['A', 'B', 'C', 'D']:
            print(f"  列{col.get('source_cols')} - head: {col.get('head')}, len: {col.get('len')}")
            print(f"    前5条: {col.get('data')[:5]}")
            print(f"    后5条: {col.get('data')[-5:]}")
    
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
                
                # 验证数据
                data_len = col.get('len', 0)
                expected_len = result.get('data_row_count', 0)
                
                if data_len == expected_len:
                    print(f"  ✓ 数据长度正确: {data_len}")
                else:
                    print(f"  ✗ 数据长度错误: 期望{expected_len}, 实际{data_len}")
        
        # 详细验证A列
        print("\n" + "-" * 100)
        print("详细验证A列（固定值）")
        print("-" * 100)
        
        col_a = next((col for col in processed_column_data if col.get('head') == '会员编号'), None)
        if col_a:
            data_a = col_a.get('data', [])
            print(f"A列数据: {data_a}")
            print(f"数据长度: {len(data_a)}")
            
            # 检查是否所有值都是相同的固定值
            if len(data_a) > 0:
                first_value = data_a[0]
                all_same = all(val == first_value for val in data_a)
                
                if all_same:
                    print(f"✓ A列所有值都是固定值: {first_value}")
                else:
                    print(f"✗ A列值不一致，第一个值: {first_value}")
                    print(f"  前10个值: {data_a[:10]}")
        
        # 详细验证B列
        print("\n" + "-" * 100)
        print("详细验证B列（序号）")
        print("-" * 100)
        
        col_b = next((col for col in processed_column_data if col.get('head') == '序号'), None)
        if col_b:
            data_b = col_b.get('data', [])
            print(f"B列数据: {data_b}")
            print(f"数据长度: {len(data_b)}")
            
            # 检查是否是从1开始的序号
            if len(data_b) > 0:
                expected_sequence = list(range(1, len(data_b) + 1))
                if data_b == expected_sequence:
                    print(f"✓ B列是正确的序号序列: 1, 2, 3, ..., {len(data_b)}")
                else:
                    print(f"✗ B列序号不正确")
                    print(f"  期望: {expected_sequence[:10]}...")
                    print(f"  实际: {data_b[:10]}...")
        
        # 详细验证C列
        print("\n" + "-" * 100)
        print("详细验证C列（COPY操作）")
        print("-" * 100)
        
        col_c = next((col for col in processed_column_data if col.get('head') == 'HAWB番号'), None)
        if col_c:
            data_c = col_c.get('data', [])
            print(f"C列数据: {data_c}")
            print(f"数据长度: {len(data_c)}")
            
            # 检查是否从源列复制
            source_col_c = next((col for col in result['column_data'] if col.get('source_cols') == 'C'), None)
            if source_col_c:
                source_data_c = source_col_c.get('data', [])
                if data_c == source_data_c:
                    print(f"✓ C列数据与源列一致")
                else:
                    print(f"✗ C列数据与源列不一致")
                    print(f"  源列前5条: {source_data_c[:5]}")
                    print(f"  C列前5条: {data_c[:5]}")
        
        # 详细验证D列
        print("\n" + "-" * 100)
        print("详细验证D列（COPY操作）")
        print("-" * 100)
        
        col_d = next((col for col in processed_column_data if col.get('head') == '現地問合せ番号'), None)
        if col_d:
            data_d = col_d.get('data', [])
            print(f"D列数据: {data_d}")
            print(f"数据长度: {len(data_d)}")
            
            # 检查是否从源列复制
            source_col_d = next((col for col in result['column_data'] if col.get('source_cols') == 'D'), None)
            if source_col_d:
                source_data_d = source_col_d.get('data', [])
                if data_d == source_data_d:
                    print(f"✓ D列数据与源列一致")
                else:
                    print(f"✗ D列数据与源列不一致")
                    print(f"  源列前5条: {source_data_d[:5]}")
                    print(f"  D列前5条: {data_d[:5]}")
        
    except Exception as e:
        print(f"\n测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        db_session.close()


if __name__ == "__main__":
    test_abcd_columns()
