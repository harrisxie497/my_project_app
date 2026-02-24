"""
测试脚本：只测试customs_processor的特殊第一行生成
"""
import sys
import os
import logging

# 添加项目路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.services.customs_processor import CustomsProcessor
from app.core.database import SessionLocal

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """
    主函数：只测试特殊第一行生成
    """
    logger.info("=" * 100)
    logger.info("测试：customs_processor特殊第一行生成")
    logger.info("=" * 100)

    # 任务目录
    task_dir = r"c:\Users\harris.xie\Documents\trae_projects\japan\backend\storage\tasks\t_0a22941a"

    try:
        # 创建数据库会话
        db = SessionLocal()

        try:
            # 创建处理器实例
            header_params = {
                "mawb_no": "16003279161",
                "flight_no": "CX509",
                "arrival_date": "20251210"
            }

            logger.info(f"创建处理器 - task_dir: {task_dir}")
            logger.info(f"header_params: {header_params}")

            processor = CustomsProcessor(
                task_dir=task_dir,
                db_session=db,
                file_type='CUSTOMS',
                header_params=header_params
            )

            # 只执行步骤1和2：解析原始文件和处理表头行
            logger.info("")
            logger.info("步骤1: 解析原始文件")
            workbook, sheet, first_row, column_data, data_row_count = processor._parse_original_file()
            logger.info(f"解析完成 - 第一行: {len(first_row)}, 列数: {len(column_data)}, 数据行数: {data_row_count}")
            logger.info(f"第一行数据: {first_row}")

            logger.info("")
            logger.info("步骤2: 处理表头行")
            special_first_row = processor._process_header_row(sheet, first_row)
            logger.info(f"特殊第一行生成: {special_first_row}")

            logger.info("")
            logger.info("验证结果:")

            # 验证期望值
            expected_b1 = "MAWB NO：16003279161"
            expected_e1 = "FLIGHT NO：CX509"
            expected_h1 = "ARRIVAL DATE：20251210"

            actual_b1 = special_first_row[1] if len(special_first_row) > 1 else None
            actual_e1 = special_first_row[4] if len(special_first_row) > 4 else None
            actual_h1 = special_first_row[7] if len(special_first_row) > 7 else None

            logger.info(f"  B1: 期望='{expected_b1}', 实际='{actual_b1}'")
            logger.info(f"  E1: 期望='{expected_e1}', 实际='{actual_e1}'")
            logger.info(f"  H1: 期望='{expected_h1}', 实际='{actual_h1}'")

            all_match = True
            if actual_b1 == expected_b1:
                logger.info("  ✓ B1值正确")
            else:
                logger.warning(f"  ✗ B1值错误")
                all_match = False

            if actual_e1 == expected_e1:
                logger.info("  ✓ E1值正确")
            else:
                logger.warning(f"  ✗ E1值错误")
                all_match = False

            if actual_h1 == expected_h1:
                logger.info("  ✓ H1值正确")
            else:
                logger.warning(f"  ✗ H1值错误")
                all_match = False

            logger.info("")
            logger.info("=" * 100)
            if all_match:
                logger.info("✓ 所有验证通过!")
            else:
                logger.warning("⚠ 部分验证失败")
            logger.info("=" * 100)

        finally:
            db.close()

    except Exception as e:
        logger.error(f"测试失败: {str(e)}", exc_info=True)
        raise


if __name__ == "__main__":
    main()
