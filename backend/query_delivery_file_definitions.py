"""
查询DELIVERY的file_definitions配置
"""

import pymysql
import json
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def query_delivery_file_definitions():
    """查询DELIVERY的file_definitions配置"""
    print("=" * 100)
    print("查询DELIVERY的file_definitions配置")
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
        
        # 查询DELIVERY的file_definitions配置
        sql = """
        SELECT file_type, file_role, sheet_name, header_row, data_start_row, columns_json
        FROM file_definitions
        WHERE file_type = 'DELIVERY'
        """
        
        cursor.execute(sql)
        results = cursor.fetchall()
        
        print(f"\n找到 {len(results)} 条记录")
        
        for row in results:
            file_type, file_role, sheet_name, header_row, data_start_row, columns_json = row
            
            print(f"\n{'=' * 100}")
            print(f"file_type: {file_type}")
            print(f"file_role: {file_role}")
            print(f"sheet_name: {sheet_name}")
            print(f"header_row: {header_row}")
            print(f"data_start_row: {data_start_row}")
            print(f"columns_json: {columns_json}")
        
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
    query_delivery_file_definitions()
