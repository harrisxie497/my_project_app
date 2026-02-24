"""
测试脚本：读取Excel文件并按列写入（包含特殊第一行）
"""
import sys
import os
import logging

# 添加项目路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.services.excel_reader import read_excel_file
from app.services.excel_writer import write_excel_file_by_columns

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """
    主函数：测试读取并写入Excel文件（包含特殊第一行）
    """
    logger.info("=" * 100)
    logger.info("测试：读取Excel并按列写入（包含特殊第一行）")
    logger.info("=" * 100)

    # 输入文件路径
    input_file = r"c:\Users\harris.xie\Documents\trae_projects\japan\backend\storage\tasks\t_0a22941a\original.xlsx"
    # 输出文件路径
    output_file = r"c:\Users\harris.xie\Documents\trae_projects\japan\backend\test_output_with_special_row.xlsx"

    try:
        logger.info("")
        logger.info("步骤1: 读取Excel文件")
        logger.info("=" * 100)

        # 读取Excel文件
        result = read_excel_file(
            input_file,
            file_type='CUSTOMS',
            file_role='SOURCE'
        )

        first_row = result["first_row"]
        column_data = result["column_data"]
        data_row_count = result["data_row_count"]

        logger.info(f"读取完成 - 特殊第一行: {len(first_row)} 列")
        logger.info(f"读取完成 - 列数: {len(column_data)}, 数据行数: {data_row_count}")

        # 显示特殊第一行的前5个值
        logger.info("")
        logger.info("特殊第一行数据（前5个）:")
        for idx, val in enumerate(first_row[:5]):
            logger.info(f"  [{idx}]: {val}")

        logger.info("")
        logger.info("=" * 100)
        logger.info("步骤2: 准备按列写入")
        logger.info("=" * 100)

        # 提取表头
        headers = [col['head'] for col in column_data]
        logger.info(f"表头数量: {len(headers)}")

        # 构建按列数据字典
        column_data_dict = {}
        for col in column_data:
            col_name = col['head']
            col_values = col['data']
            column_data_dict[col_name] = col_values

        logger.info(f"列数据字典数量: {len(column_data_dict)}")

        # 显示每列的数据长度
        logger.info("")
        logger.info("各列数据长度:")
        for idx, col in enumerate(column_data, 1):
            col_name = col['head']
            data_len = col['len']
            logger.info(f"  {idx}. {col_name}: {data_len} 行")

        logger.info("")
        logger.info("=" * 100)
        logger.info("步骤3: 按列写入Excel文件")
        logger.info("=" * 100)
        logger.info(f"输出文件: {output_file}")
        logger.info(f"特殊第一行: {first_row[:3]}... (共{len(first_row)}列)")

        # 按列写入（包含特殊第一行）
        write_excel_file_by_columns(
            file_path=output_file,
            headers=headers,
            column_data=column_data_dict,
            special_first_row=first_row  # 写入特殊第一行
        )

        logger.info("")
        logger.info("=" * 100)
        logger.info("步骤4: 验证写入结果")
        logger.info("=" * 100)

        # 重新读取生成的文件验证
        verify_result = read_excel_file(
            output_file,
            file_type='CUSTOMS',
            file_role='SOURCE'
        )

        verify_first_row = verify_result["first_row"]
        verify_column_data = verify_result["column_data"]
        verify_data_row_count = verify_result["data_row_count"]

        logger.info(f"验证 - 特殊第一行: {len(verify_first_row)} 列")
        logger.info(f"验证 - 列数: {len(verify_column_data)}, 数据行数: {verify_data_row_count}")

        # 比较特殊第一行
        logger.info("")
        logger.info("比较特殊第一行:")
        if first_row == verify_first_row:
            logger.info("✓ 特殊第一行数据一致")
        else:
            logger.warning("⚠ 特殊第一行数据不一致")
            for idx in range(min(len(first_row), len(verify_first_row))):
                if first_row[idx] != verify_first_row[idx]:
                    logger.warning(f"  列{idx}: 原始={first_row[idx]}, 验证={verify_first_row[idx]}")

        # 比较数据行数
        logger.info("")
        logger.info("比较数据行数:")
        if data_row_count == verify_data_row_count:
            logger.info(f"✓ 数据行数一致: {data_row_count}")
        else:
            logger.warning(f"⚠ 数据行数不一致: 原始={data_row_count}, 验证={verify_data_row_count}")

        # 比较列数
        logger.info("")
        logger.info("比较列数:")
        if len(column_data) == len(verify_column_data):
            logger.info(f"✓ 列数一致: {len(column_data)}")
        else:
            logger.warning(f"⚠ 列数不一致: 原始={len(column_data)}, 验证={len(verify_column_data)}")

        logger.info("")
        logger.info("=" * 100)
        logger.info("✓ 测试完成!")
        logger.info(f"✓ 输出文件: {output_file}")
        logger.info("=" * 100)

    except Exception as e:
        logger.error(f"测试失败: {str(e)}", exc_info=True)
        raise


if __name__ == "__main__":
    main()
