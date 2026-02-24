"""
查询tasks表，看看是否有header_params字段
"""

import pymysql
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def query_tasks_table():
    """查询tasks表"""
    print("=" * 100)
    print("查询tasks表")
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
        
        # 查询tasks表的结构
        sql = "DESCRIBE tasks"
        cursor.execute(sql)
        results = cursor.fetchall()
        
        print(f"\ntasks表的结构：")
        for row in results:
            field, type, null, key, default, extra = row
            print(f"  {field}: {type}")
        
        # 查询tasks表的数据
        sql = "SELECT * FROM tasks LIMIT 1"
        cursor.execute(sql)
        results = cursor.fetchall()
        
        print(f"\ntasks表的数据（前1条）：")
        for row in results:
            print(f"  {row}")
        
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
    query_tasks_table()
