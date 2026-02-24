"""
查询D列和F列的配置
"""

import pymysql
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def query_d_and_f_columns_config():
    """查询D列和F列的配置"""
    print("=" * 100)
    print("查询D列和F列的配置")
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
        SELECT target_col, target_header, map_op, source_cols, field_type, rule_ref, depends_on, enabled
        FROM field_pipelines
        WHERE file_type = 'CUSTOMS' AND target_col = 'D'
        """
        
        cursor.execute(sql)
        results = cursor.fetchall()
        
        print(f"\n找到 {len(results)} 条记录")
        
        for row in results:
            target_col, target_header, map_op, source_cols, field_type, rule_ref, depends_on, enabled = row
            
            print(f"\n{'=' * 100}")
            print(f"target_col: {target_col}")
            print(f"target_header: {target_header}")
            print(f"map_op: {map_op}")
            print(f"source_cols: {source_cols}")
            print(f"field_type: {field_type}")
            print(f"rule_ref: {rule_ref}")
            print(f"depends_on: {depends_on}")
            print(f"enabled: {enabled}")
        
        # 查询F列的配置
        sql = """
        SELECT target_col, target_header, map_op, source_cols, field_type, rule_ref, depends_on, enabled
        FROM field_pipelines
        WHERE file_type = 'CUSTOMS' AND target_col = 'F'
        """
        
        cursor.execute(sql)
        results = cursor.fetchall()
        
        print(f"\n找到 {len(results)} 条记录")
        
        for row in results:
            target_col, target_header, map_op, source_cols, field_type, rule_ref, depends_on, enabled = row
            
            print(f"\n{'=' * 100}")
            print(f"target_col: {target_col}")
            print(f"target_header: {target_header}")
            print(f"map_op: {map_op}")
            print(f"source_cols: {source_cols}")
            print(f"field_type: {field_type}")
            print(f"rule_ref: {rule_ref}")
            print(f"depends_on: {depends_on}")
            print(f"enabled: {enabled}")
        
        # 关闭连接
        cursor.close()
        connection.close()
        
        print("\n" + "=" * 100)
        print("查询完成！")
        print("=" * 100)
        
    except Exception as e:
        print(f"\n❌ 查询失败: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    query_d_and_f_columns_config()
