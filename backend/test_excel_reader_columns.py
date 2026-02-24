"""
测试脚本：读取真实Excel文件并按列组织数据
"""
import sys
import os
import logging

# 添加项目路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.services.excel_reader import read_excel_file

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """
    主函数：测试Excel读取和按列组织数据
    """
    logger.info("=" * 100)
    logger.info("开始测试：读取Excel文件并按列组织数据")
    logger.info("=" * 100)

    # 真实Excel文件路径
    file_path = r"c:\Users\harris.xie\Documents\trae_projects\japan\backend\storage\tasks\t_0a22941a\original.xlsx"

    try:
        logger.info(f"读取文件: {file_path}")
        logger.info(f"文件类型: CUSTOMS")
        logger.info(f"文件角色: SOURCE")
        logger.info("")

        # 读取Excel文件
        result = read_excel_file(
            file_path,
            file_type='CUSTOMS',
            file_role='SOURCE'
        )

        # 提取结果
        first_row = result["first_row"]
        column_data = result["column_data"]
        data_row_count = result["data_row_count"]

        # 输出第一行（特殊行）
        logger.info("=" * 100)
        logger.info("第一行（特殊行）数据:")
        logger.info("=" * 100)
        logger.info(f"列数: {len(first_row)}")
        for idx, value in enumerate(first_row):
            logger.info(f"  列{idx}: {value}")
        logger.info("")

        # 输出按列组织的数据
        logger.info("=" * 100)
        logger.info("按列组织的数据:")
        logger.info("=" * 100)
        logger.info(f"总列数: {len(column_data)}")
        logger.info(f"总数据行数: {data_row_count}")
        logger.info("")

        # 详细输出每列信息
        for idx, col in enumerate(column_data, 1):
            source_cols = col.get('source_cols')
            head = col.get('head')
            data = col.get('data', [])
            length = col.get('len')

            logger.info(f"列 {idx}/{len(column_data)}:")
            logger.info(f"  源列: {source_cols}")
            logger.info(f"  表头: {head}")
            logger.info(f"  数据长度: {length}")

            # 显示前5个和后5个数据
            if data:
                logger.info(f"  前5个值:")
                for i, val in enumerate(data[:5]):
                    val_str = str(val)[:50] if val is not None else "None"
                    logger.info(f"    行{i+1}: {val_str}")

                if length > 10:
                    logger.info(f"  ... 中间省略 {length - 10} 行 ...")
                    logger.info(f"  后5个值:")
                    for i, val in enumerate(data[-5:], start=length-4):
                        val_str = str(val)[:50] if val is not None else "None"
                        logger.info(f"    行{i}: {val_str}")
            else:
                logger.info(f"  数据为空")

            logger.info("")

        # 验证数据一致性
        logger.info("=" * 100)
        logger.info("数据一致性验证:")
        logger.info("=" * 100)
        lengths = [col.get('len', 0) for col in column_data]
        unique_lengths = set(lengths)

        if len(unique_lengths) == 1:
            logger.info(f"✓ 所有列数据长度一致: {list(unique_lengths)[0]} 行")
        else:
            logger.warning(f"⚠ 列数据长度不一致:")
            for length in sorted(unique_lengths):
                cols_with_len = [col.get('source_cols') for col in column_data if col.get('len') == length]
                logger.warning(f"  长度 {length}: {', '.join(cols_with_len)}")

        logger.info("")
        logger.info("=" * 100)
        logger.info("测试完成!")
        logger.info("=" * 100)

    except Exception as e:
        logger.error(f"测试失败: {str(e)}", exc_info=True)
        raise


if __name__ == "__main__":
    main()
