"""
检查数据库中的D列配置
"""

import pymysql
import logging
import json

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def check_d_column_config():
    """检查数据库中的D列配置"""
    print("=" * 100)
    print("检查数据库中的D列配置")
    print("=" * 100)
    
    # 数据库连接配置
    db_config = {
        'host': '172.18.207.224',
        'port': 3306,
        'user': 'app',
        'password': 'app123456',
        'database': 'demo',
        'charset': 'utf8mb4'
    }
    
    try:
        # 连接数据库
        connection = pymysql.connect(**db_config)
        cursor = connection.cursor()
        
        # 查询D列的配置
        sql = """
        SELECT id, target_col, map_op, source_cols, field_type, rule_ref, depends_on, enabled
        FROM field_pipelines
        WHERE target_col = 'D'
          AND file_type = 'CUSTOMS'
          AND map_op = 'COPY'
          AND field_type = 'CALC'
          AND rule_ref LIKE '%policy_copy_equal_to%'
        """
        
        cursor.execute(sql)
        results = cursor.fetchall()
        
        print(f"\n找到 {len(results)} 条记录：")
        for row in results:
            print(f"\nID: {row[0]}")
            print(f"  target_col: {row[1]}")
            print(f"  map_op: {row[2]}")
            print(f"  source_cols: {row[3]}")
            print(f"  field_type: {row[4]}")
            print(f"  rule_ref: {row[5]}")
            print(f"  depends_on: {row[6]}")
            print(f"  enabled: {row[7]}")
        
        # 关闭连接
        cursor.close()
        connection.close()
        
        print("\n检查完成！")
        
    except Exception as e:
        print(f"\n检查失败: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    check_d_column_config()
