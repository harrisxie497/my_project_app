"""
从MySQL导入数据到SQLite
"""
import sys
import os
import logging
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.core.database import SessionLocal
from app.models import field_pipeline, rule_definition, file_definition
from sqlalchemy import text
import uuid

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def import_from_mysql():
    """
    从MySQL数据库导入数据到SQLite
    """
    logger.info("开始从MySQL导入数据...")

    # MySQL连接配置
    mysql_config = {
        'host': '172.18.207.224',
        'port': 3306,
        'user': 'app',
        'password': 'app123456',
        'database': 'demo',
        'charset': 'utf8mb4'
    }

    try:
        import pymysql

        # 连接MySQL
        mysql_conn = pymysql.connect(**mysql_config)
        logger.info("MySQL连接成功")

        # 连接SQLite
        sqlite_db = SessionLocal()
        logger.info("SQLite连接成功")

        # 导入 field_pipelines
        logger.info("=" * 100)
        logger.info("导入 field_pipelines...")
        logger.info("=" * 100)

        with mysql_conn.cursor() as cursor:
            cursor.execute("SELECT * FROM field_pipelines WHERE file_type = 'CUSTOMS'")
            rows = cursor.fetchall()

            # 获取列名
            columns = [desc[0] for desc in cursor.description]
            logger.info(f"MySQL中的field_pipelines列: {columns}")
            logger.info(f"获取到 {len(rows)} 条记录")

            for row in rows:
                row_dict = dict(zip(columns, row))
                logger.info(f"导入: {row_dict['target_col']} - {row_dict['target_header']}")

                # 创建SQLite记录
                pipeline = field_pipeline.FieldPipeline(
                    file_type=row_dict['file_type'],
                    target_col=row_dict['target_col'],
                    target_header=row_dict['target_header'],
                    map_op=row_dict['map_op'],
                    source_cols=json.loads(row_dict['source_cols']) if isinstance(row_dict['source_cols'], str) else row_dict['source_cols'],
                    field_type=row_dict['field_type'],
                    rule_ref=json.loads(row_dict['rule_ref']) if isinstance(row_dict['rule_ref'], str) else row_dict['rule_ref'],
                    rule_params_json=json.loads(row_dict['rule_params_json']) if isinstance(row_dict['rule_params_json'], str) else row_dict['rule_params_json'],
                    depends_on=json.loads(row_dict['depends_on']) if isinstance(row_dict['depends_on'], str) else row_dict['depends_on'],
                    order_num=row_dict['order_num'],
                    enabled=row_dict['enabled']
                )
                sqlite_db.add(pipeline)

            sqlite_db.commit()
            logger.info(f"成功导入 {len(rows)} 条field_pipelines记录")

        # 导入 rule_definitions
        logger.info("=" * 100)
        logger.info("导入 rule_definitions...")
        logger.info("=" * 100)

        with mysql_conn.cursor() as cursor:
            cursor.execute("SELECT * FROM rule_definitions")
            rows = cursor.fetchall()

            columns = [desc[0] for desc in cursor.description]
            logger.info(f"MySQL中的rule_definitions列: {columns}")
            logger.info(f"获取到 {len(rows)} 条记录")

            for row in rows:
                row_dict = dict(zip(columns, row))
                logger.info(f"导入: {row_dict['rule_ref']}")

                # 创建SQLite记录
                rule = rule_definition.RuleDefinition(
                    rule_ref=row_dict['rule_ref'],
                    rule_type=row_dict['rule_type'],
                    executor_type=row_dict['executor_type'],
                    schema_json=json.loads(row_dict['schema_json']) if isinstance(row_dict['schema_json'], str) else row_dict['schema_json'],
                    enabled=row_dict['enabled']
                )
                sqlite_db.add(rule)

            sqlite_db.commit()
            logger.info(f"成功导入 {len(rows)} 条rule_definitions记录")

        # 导入 file_definitions
        logger.info("=" * 100)
        logger.info("导入 file_definitions...")
        logger.info("=" * 100)

        with mysql_conn.cursor() as cursor:
            cursor.execute("SELECT * FROM file_definitions")
            rows = cursor.fetchall()

            columns = [desc[0] for desc in cursor.description]
            logger.info(f"MySQL中的file_definitions列: {columns}")
            logger.info(f"获取到 {len(rows)} 条记录")

            for row in rows:
                row_dict = dict(zip(columns, row))
                logger.info(f"导入: {row_dict['file_type']} - {row_dict['file_role']}")

                # 创建SQLite记录
                file_def = file_definition.FileDefinition(
                    id=str(uuid.uuid4()),  # 生成UUID
                    file_type=row_dict['file_type'],
                    file_role=row_dict['file_role'],
                    columns_json=json.loads(row_dict['columns_json']) if isinstance(row_dict['columns_json'], str) else row_dict['columns_json'],
                    header_row=row_dict['header_row'],
                    data_start_row=row_dict['data_start_row']
                )
                sqlite_db.add(file_def)

            sqlite_db.commit()
            logger.info(f"成功导入 {len(rows)} 条file_definitions记录")

        mysql_conn.close()
        sqlite_db.close()

        logger.info("=" * 100)
        logger.info("数据导入完成！")
        logger.info("=" * 100)

    except Exception as e:
        logger.error(f"导入失败: {str(e)}", exc_info=True)
        raise


if __name__ == "__main__":
    import_from_mysql()
