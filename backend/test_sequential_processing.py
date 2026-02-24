"""
测试脚本：按照 order_num 顺序逐列处理数据
"""
import sys
import os
import logging
from datetime import datetime

# 添加项目路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.services.excel_reader import read_excel_file
from app.services.field_handlers_v2 import process_field_v2
from app.services.deepseek_ai_service import DeepSeekAIService
from app.core.database import SessionLocal
from app.models.field_pipeline import FieldPipeline

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def get_field_pipelines(db_session):
    """
    获取字段处理配置，按 order_num 排序

    Args:
        db_session: 数据库会话

    Returns:
        字段处理配置列表
    """
    pipelines = db_session.query(FieldPipeline).filter(
        FieldPipeline.file_type == 'CUSTOMS',
        FieldPipeline.enabled == True
    ).order_by(FieldPipeline.order_num).all()

    result = []
    for pipeline in pipelines:
        result.append({
            'target_col': pipeline.target_col,
            'target_header': pipeline.target_header,
            'map_op': pipeline.map_op,
            'source_cols': pipeline.source_cols,
            'field_type': pipeline.field_type,
            'rule_ref': pipeline.rule_ref,
            'rule_params_json': pipeline.rule_params_json,
            'depends_on': pipeline.depends_on,
            'order_num': pipeline.order_num
        })

    logger.info(f"获取到 {len(result)} 个字段处理配置")
    return result


def process_columns_sequentially(file_path, pipelines, column_data, data_row_count):
    """
    按照 order_num 顺序逐列处理数据

    Args:
        file_path: Excel文件路径
        pipelines: 字段处理配置列表（已按 order_num 排序）
        column_data: 原始列数据
        data_row_count: 数据行数

    Returns:
        处理后的列数据
    """
    # 初始化AI服务
    ai_service = None
    ai_configured = False

    try:
        from app.core.config import settings
        api_key = getattr(settings, 'DEEPSEEK_API_KEY', '')
        if api_key:
            base_url = getattr(settings, 'DEEPSEEK_API_URL', 'https://api.deepseek.com/v1')
            ai_service = DeepSeekAIService(api_key, base_url)
            ai_configured = True
            logger.info("AI服务已初始化")
        else:
            logger.warning("DEEPSEEK_API_KEY 未配置，AI功能将不可用")
    except Exception as e:
        logger.warning(f"AI服务初始化失败：{str(e)}")

    # 当前时间
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # 处理结果存储
    processed_column_data_map = {}
    processed_columns = set()

    # 按 order_num 顺序处理每列
    for idx, pipeline in enumerate(pipelines, 1):
        target_col = pipeline.get('target_col')
        target_header = pipeline.get('target_header')
        order_num = pipeline.get('order_num')
        map_op = pipeline.get('map_op')
        source_cols = pipeline.get('source_cols', [])
        field_type = pipeline.get('field_type')
        rule_ref = pipeline.get('rule_ref', [])
        depends_on = pipeline.get('depends_on', [])

        logger.info("=" * 100)
        logger.info(f"处理列 {idx}/{len(pipelines)} - order_num: {order_num}")
        logger.info(f"  目标列: {target_col} ({target_header})")
        logger.info(f"  映射操作: {map_op}, 字段类型: {field_type}")
        logger.info(f"  源列: {source_cols}, 规则引用: {rule_ref}")
        logger.info(f"  依赖列: {depends_on}")
        logger.info("=" * 100)

        # 检查依赖
        dependencies_met = True
        for dep_col in depends_on:
            if dep_col not in processed_columns:
                dependencies_met = False
                logger.warning(f"  依赖未满足 - {dep_col} 未处理，跳过此列")
                break

        if not dependencies_met:
            continue

        # 查找源列数据
        source_column_data = None
        source_column_info = None

        if source_cols:
            for col in column_data:
                if col.get('source_cols') == source_cols[0]:
                    source_column_data = col.get('data', [])
                    source_column_info = col
                    break
        else:
            # CONST 或无源列的情况，使用 data_row_count
            source_column_data = list(range(data_row_count))

        if not source_column_data and source_cols:
            logger.warning(f"  源列数据未找到: {source_cols[0]}")
            continue

        # 限制数据行数
        source_column_data = source_column_data[:data_row_count]

        if source_cols:
            logger.info(f"  源列: {source_cols[0]}, 数据行数: {len(source_column_data)}")
        else:
            logger.info(f"  无源列（CONST/CALC类型）, 数据行数: {len(source_column_data)}")

        # 构建列数据映射
        column_data_map = {}
        for col in column_data:
            col_source_cols = col.get('source_cols')
            if col_source_cols:
                column_data_map[col_source_cols] = col.get('data', [])[:data_row_count]

        # 添加已处理列的数据
        for processed_col in processed_columns:
            if processed_col in processed_column_data_map:
                column_data_map[processed_col] = processed_column_data_map[processed_col]

        # 逐行处理
        processed_values = []
        sample_results = []

        for row_idx in range(len(source_column_data)):
            # 构建行数据
            row = {}
            row['_row_index'] = row_idx

            # 添加源列数据
            if source_cols:
                for col in source_cols:
                    if col in column_data_map:
                        row[col] = column_data_map[col][row_idx] if row_idx < len(column_data_map[col]) else None

            # 添加依赖列数据
            for dep_col in depends_on:
                if dep_col in column_data_map:
                    row[dep_col] = column_data_map[dep_col][row_idx] if row_idx < len(column_data_map[dep_col]) else None

            # 处理字段
            try:
                result = process_field_v2(
                    map_op=map_op,
                    source_cols=source_cols,
                    field_type=field_type,
                    rule_ref=rule_ref,
                    row=row,
                    pipeline=pipeline,
                    exchange_rate_service=None,
                    ai_service=ai_service,
                    current_time=current_time
                )
                processed_values.append(result)

                # 收集前5行作为示例
                if row_idx < 5:
                    sample_results.append({
                        'row': row_idx + 1,
                        'source': row.get(source_cols[0], ''),
                        'result': result
                    })

            except Exception as e:
                logger.error(f"  处理行 {row_idx + 1} 失败: {str(e)}")
                processed_values.append(None)

        # 保存处理结果
        processed_column_data_map[target_col] = processed_values
        processed_columns.add(target_col)

        # 输出处理结果摘要
        logger.info(f"  处理完成 - 数据行数: {len(processed_values)}")
        logger.info(f"  示例结果（前5行）:")
        for sample in sample_results:
            source_val = sample['source']
            result_val = sample['result']
            source_str = str(source_val)[:30] if source_val else 'N/A'
            result_str = str(result_val)[:30] if result_val else 'None'
            logger.info(f"    行{sample['row']}: {source_str} -> {result_str}")

        logger.info("")

    return processed_column_data_map


def main():
    """
    主函数：执行逐列处理测试
    """
    logger.info("=" * 100)
    logger.info("开始测试：逐列处理数据")
    logger.info("=" * 100)

    # 数据库会话
    db = SessionLocal()

    try:
        # 1. 读取Excel文件
        file_path = r"c:\Users\harris.xie\Documents\trae_projects\japan\backend\storage\tasks\t_0a22941a\original.xlsx"

        logger.info("")
        logger.info("=" * 100)
        logger.info("步骤1: 读取Excel文件")
        logger.info("=" * 100)

        result = read_excel_file(
            file_path,
            file_type='CUSTOMS',
            file_role='SOURCE'
        )

        first_row = result["first_row"]
        column_data = result["column_data"]
        data_row_count = result["data_row_count"]

        logger.info(f"读取完成 - 第一行数据: {first_row}")
        logger.info(f"读取完成 - 列数: {len(column_data)}, 数据行数: {data_row_count}")

        # 2. 获取字段处理配置
        logger.info("")
        logger.info("=" * 100)
        logger.info("步骤2: 获取字段处理配置")
        logger.info("=" * 100)

        pipelines = get_field_pipelines(db)

        logger.info(f"配置信息:")
        for idx, pipeline in enumerate(pipelines, 1):
            logger.info(f"  {idx}. order_num={pipeline['order_num']}, "
                       f"target_col={pipeline['target_col']} ({pipeline['target_header']}), "
                       f"map_op={pipeline['map_op']}, "
                       f"rule_ref={pipeline['rule_ref']}")

        # 3. 逐列处理
        logger.info("")
        logger.info("=" * 100)
        logger.info("步骤3: 逐列处理数据")
        logger.info("=" * 100)

        processed_data = process_columns_sequentially(file_path, pipelines, column_data, data_row_count)

        # 4. 输出最终结果
        logger.info("")
        logger.info("=" * 100)
        logger.info("步骤4: 输出最终结果")
        logger.info("=" * 100)

        logger.info(f"处理完成 - 共处理 {len(processed_data)} 列")
        logger.info("")

        for col_name, values in processed_data.items():
            logger.info(f"列 {col_name}:")
            logger.info(f"  数据行数: {len(values)}")
            logger.info(f"  前5个值: {values[:5]}")
            logger.info(f"  后5个值: {values[-5:]}")
            logger.info("")

        logger.info("=" * 100)
        logger.info("测试完成")
        logger.info("=" * 100)

    except Exception as e:
        logger.error(f"测试失败: {str(e)}", exc_info=True)
        raise

    finally:
        db.close()


if __name__ == "__main__":
    main()
