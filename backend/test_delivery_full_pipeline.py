"""DELIVERY全流程测试 - 从excel_read到excel_write"""
import os
import sys
import logging

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.services.excel_reader import read_excel_file
from app.services.excel_writer import write_excel_file_by_columns
from app.services.delivery_processor import DeliveryProcessor
from app.core.database import SessionLocal

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def test_delivery_full_pipeline():
    """测试DELIVERY全流程"""
    print("=" * 100)
    print("DELIVERY全流程测试")
    print("=" * 100)

    # 测试目录
    test_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_results")
    os.makedirs(test_dir, exist_ok=True)

    # 源文件路径
    source_file = os.path.join(test_dir, "delivery_original.xlsx")
    if not os.path.exists(source_file):
        print(f"Error: Source file not found: {source_file}")
        return False

    print(f"\n1. 读取Excel文件 (excel_reader)")
    print("-" * 100)

    # 读取Excel文件
    try:
        result = read_excel_file(source_file, file_type='DELIVERY', file_role='SOURCE')
        print(f"  工作表: {result['worksheet'].title}")
        print(f"  第一行: {result['first_row']}")
        print(f"  数据行数: {result['data_row_count']}")
        print(f"  列数: {len(result['column_data'])}")
        print(f"  列名: {[col['head'] for col in result['column_data']]}")
        print("  [OK] Excel文件读取成功")
    except Exception as e:
        print(f"  [FAIL] Excel文件读取失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

    print(f"\n2. 创建DeliveryProcessor并处理数据")
    print("-" * 100)

    # 创建DeliveryProcessor
    try:
        header_params = {
            'mawb_no': 'MAWB20260207001',
            'flight_no': 'JL123',
            'arrival_date': '2026-02-08'
        }

        processor = DeliveryProcessor(
            task_dir=test_dir,
            db_session=SessionLocal(),
            file_type='DELIVERY',
            header_params=header_params
        )

        # 设置源文件
        processor.original_file_path = source_file
        processor.result_file_path = os.path.join(test_dir, "delivery_result.xlsx")

        # 处理数据
        stats = processor.process()
        print(f"  处理统计: {stats}")
        print("  [OK] DeliveryProcessor处理成功")
    except Exception as e:
        print(f"  [FAIL] DeliveryProcessor处理失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

    print(f"\n3. 验证结果文件")
    print("-" * 100)

    # 验证结果文件
    result_file = processor.result_file_path
    if os.path.exists(result_file):
        print(f"  [OK] 结果文件已生成: {result_file}")

        # 读取结果文件验证
        try:
            result_data = read_excel_file(result_file, file_type='DELIVERY', file_role='OUTPUT')
            print(f"  结果文件列数: {len(result_data['column_data'])}")
            print(f"  结果文件数据行数: {result_data['data_row_count']}")
            print(f"  结果文件列名: {[col['head'] for col in result_data['column_data']]}")

            # 验证数据
            print("\n4. 数据验证")
            print("-" * 100)

            original_col_data = result['column_data']
            result_col_data = result_data['column_data']

            # 比较每个列
            for orig_col, res_col in zip(original_col_data, result_col_data):
                orig_data = orig_col['data']
                res_data = res_col['data']

                print(f"\n  列: {orig_col['head']}")
                print(f"    原始数据行数: {len(orig_data)}")
                print(f"    结果数据行数: {len(res_data)}")

                # 检查数据一致性
                if len(orig_data) == len(res_data):
                    match_count = sum(1 for o, r in zip(orig_data, res_data) if o == r)
                    print(f"    匹配: {match_count}/{len(orig_data)}")
                    if match_count == len(orig_data):
                        print(f"    [OK] 数据完全一致")
                    else:
                        print(f"    [WARN] 数据有差异")

                        # 显示差异
                        for i, (o, r) in enumerate(zip(orig_data, res_data)):
                            if o != r:
                                print(f"      行{i+2}: 原始={repr(o)}, 结果={repr(r)}")
                else:
                    print(f"    [WARN] 数据行数不一致")

            print("\n  [OK] 数据验证完成")

        except Exception as e:
            print(f"  [WARN] 验证结果文件失败: {str(e)}")
    else:
        print(f"  [FAIL] 结果文件未生成: {result_file}")
        return False

    print("\n" + "=" * 100)
    print("DELIVERY全流程测试完成!")
    print("=" * 100)
    return True

if __name__ == "__main__":
    success = test_delivery_full_pipeline()
    sys.exit(0 if success else 1)
