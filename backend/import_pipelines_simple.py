"""
简化版导入脚本 - 只导入 field_pipelines
"""
import sys
import os
import logging
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.core.database import SessionLocal
from app.models import field_pipeline

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def import_field_pipelines():
    """
    只导入 field_pipelines
    """
    logger.info("开始导入 field_pipelines...")

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
        mysql_conn = pymysql.connect(**mysql_config)
        sqlite_db = SessionLocal()

        with mysql_conn.cursor() as cursor:
            cursor.execute("SELECT * FROM field_pipelines WHERE file_type = 'CUSTOMS' ORDER BY order_num")
            rows = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]

            logger.info(f"获取到 {len(rows)} 条记录")
            logger.info(f"列: {columns}")

            for row in rows:
                row_dict = dict(zip(columns, row))
                target_col = row_dict['target_col']
                target_header = row_dict['target_header']
                order_num = row_dict['order_num']

                logger.info(f"导入 #{order_num}: {target_col} - {target_header}")

                try:
                    # 解析JSON字段
                    source_cols = row_dict['source_cols']
                    if isinstance(source_cols, str):
                        source_cols = json.loads(source_cols)

                    rule_ref = row_dict['rule_ref']
                    if isinstance(rule_ref, str):
                        rule_ref = json.loads(rule_ref)

                    rule_params_json = row_dict['rule_params_json']
                    if isinstance(rule_params_json, str):
                        rule_params_json = json.loads(rule_params_json)

                    depends_on = row_dict['depends_on']
                    if isinstance(depends_on, str):
                        depends_on = json.loads(depends_on)

                    pipeline = field_pipeline.FieldPipeline(
                        file_type=row_dict['file_type'],
                        target_col=target_col,
                        target_header=target_header,
                        map_op=row_dict['map_op'],
                        source_cols=source_cols,
                        field_type=row_dict['field_type'],
                        rule_ref=rule_ref,
                        rule_params_json=rule_params_json,
                        depends_on=depends_on,
                        order_num=order_num,
                        enabled=row_dict['enabled']
                    )
                    sqlite_db.add(pipeline)

                except Exception as e:
                    logger.error(f"导入失败 {target_col}: {str(e)}")
                    continue

            sqlite_db.commit()
            logger.info(f"成功导入记录")

        mysql_conn.close()
        sqlite_db.close()

        logger.info("导入完成！")

    except Exception as e:
        logger.error(f"导入失败: {str(e)}", exc_info=True)
        raise


if __name__ == "__main__":
    import_field_pipelines()
