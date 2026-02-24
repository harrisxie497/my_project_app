"""
检查被DROP的列的field_pipelines配置
"""

import pymysql
import json
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def check_dropped_columns():
    """检查被DROP的列的field_pipelines配置"""
    print("=" * 100)
    print("检查被DROP的列的field_pipelines配置")
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
        
        # 查询被DROP的列的field_pipelines配置
        sql = """
        SELECT target_col, map_op, source_cols, field_type, rule_ref, depends_on, enabled
        FROM field_pipelines
        WHERE file_type = 'CUSTOMS'
          AND (map_op = 'NONE' OR map_op = 'DROP')
          AND enabled = 1
        ORDER BY target_col
        """
        
        cursor.execute(sql)
        results = cursor.fetchall()
        
        print(f"\n找到 {len(results)} 个被DROP的列")
        
        for row in results:
            target_col, map_op, source_cols, field_type, rule_ref, depends_on, enabled = row
            
            print(f"\n{'=' * 100}")
            print(f"列名: {target_col}")
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
        print("检查完成！")
        print("=" * 100)
        
    except Exception as e:
        print(f"\n❌ 检查失败: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    check_dropped_columns()
