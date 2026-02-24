"""
修复D列的配置，将source_cols从空数组改为['C']
"""

import pymysql
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def fix_d_column_config():
    """修复D列的配置"""
    print("=" * 100)
    print("修复D列的配置")
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
        
        # 执行SQL语句
        sql = """
        UPDATE field_pipelines
        SET source_cols = '["C"]'
        WHERE target_col = 'D'
          AND file_type = 'CUSTOMS'
          AND map_op = 'COPY'
          AND field_type = 'CALC'
          AND rule_ref LIKE '%policy_copy_equal_to%'
          AND enabled = 1
        """
        
        cursor.execute(sql)
        connection.commit()
        
        # 查看更新后的记录数
        cursor.execute("SELECT ROW_COUNT()")
        row_count = cursor.fetchone()[0]
        
        print(f"\n成功更新 {row_count} 条记录")
        
        # 关闭连接
        cursor.close()
        connection.close()
        
        print("\n修复完成！")
        
    except Exception as e:
        print(f"\n修复失败: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    fix_d_column_config()
