"""
测试脚本：验证process_header_row函数的返回值
"""
import sys
import os
import logging

# 添加项目路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.services.header_processor import process_header_row

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """
    主函数：测试process_header_row函数
    """
    logger.info("=" * 100)
    logger.info("测试：process_header_row函数返回值")
    logger.info("=" * 100)

    try:
        # 测试数据
        header_params = {
            "mawb_no": "16003279161",
            "flight_no": "CX509",
            "arrival_date": "20251210"
        }

        logger.info("")
        logger.info("测试参数:")
        logger.info(f"  mawb_no: {header_params['mawb_no']}")
        logger.info(f"  flight_no: {header_params['flight_no']}")
        logger.info(f"  arrival_date: {header_params['arrival_date']}")
        logger.info("")

        # 调用函数（默认8列）
        logger.info("调用 process_header_row（默认8列）:")
        result = process_header_row(header_params)

        logger.info("")
        logger.info("返回结果:")
        logger.info(f"  类型: {type(result)}")
        logger.info(f"  长度: {len(result)}")
        logger.info("")

        # 显示完整列表
        logger.info("完整列表:")
        for idx, val in enumerate(result):
            val_repr = f'"{val}"' if val else "''"
            logger.info(f"  [{idx}]: {val_repr} (列{'ABCDEFGH'[idx] if idx < 8 else '?'})")

        logger.info("")

        # 验证期望值
        logger.info("=" * 100)
        logger.info("验证期望值:")
        logger.info("=" * 100)

        expected_result = ["", "MAWB NO：16003279161", "", "", "FLIGHT NO：CX509", "", "", "ARRIVAL DATE：20251210"]

        if result == expected_result:
            logger.info("✓ 返回值与期望值完全一致")
        else:
            logger.warning("⚠ 返回值与期望值不一致")
            for idx in range(max(len(result), len(expected_result))):
                expected = expected_result[idx] if idx < len(expected_result) else "N/A"
                actual = result[idx] if idx < len(result) else "N/A"
                if expected != actual:
                    logger.warning(f"  索引{idx}: 期望={expected}, 实际={actual}")

        logger.info("")

        # 测试不同列数
        logger.info("=" * 100)
        logger.info("测试不同列数:")
        logger.info("=" * 100)

        for cols in [8, 10, 42]:
            logger.info(f"测试 {cols} 列:")
            result_cols = process_header_row(header_params, total_columns=cols)
            logger.info(f"  返回长度: {len(result_cols)}")
            logger.info(f"  前8列: {result_cols[:8]}")
            logger.info("")

        logger.info("")
        logger.info("=" * 100)
        logger.info("✓ 测试完成!")
        logger.info("=" * 100)

    except Exception as e:
        logger.error(f"测试失败: {str(e)}", exc_info=True)
        raise


if __name__ == "__main__":
    main()
