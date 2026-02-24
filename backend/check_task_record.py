"""
检查task_record中的unique_code、flight_no、declare_date字段是否有值
"""

import pymysql
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def check_task_record():
    """检查task_record中的unique_code、flight_no、declare_date字段是否有值"""
    print("=" * 100)
    print("检查task_record中的unique_code、flight_no、declare_date字段是否有值")
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
        
        # 查询task记录
        sql = """
        SELECT id, unique_code, flight_no, declare_date
        FROM tasks
        WHERE id = 't_0fc5b76e'
        """
        
        cursor.execute(sql)
        results = cursor.fetchall()
        
        print(f"\n找到 {len(results)} 条记录")
        
        for row in results:
            id, unique_code, flight_no, declare_date = row
            
            print(f"\n{'=' * 100}")
            print(f"ID: {id}")
            print(f"unique_code: {unique_code}")
            print(f"flight_no: {flight_no}")
            print(f"declare_date: {declare_date}")
        
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
    check_task_record()
