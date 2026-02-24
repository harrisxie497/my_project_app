"""
查询tasks表的结构
"""

import pymysql
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def query_tasks_structure():
    """查询tasks表的结构"""
    print("=" * 100)
    print("查询tasks表的结构")
    print("=" * 100)
    
    try:
        connection = pymysql.connect(
            host='172.18.207.224',
            port=3306,
            user='app',
            password='app123456',
            database='demo',
            charset='utf8mb4'
        )
        cursor = connection.cursor()
        
        # 查询tasks表的结构
        sql = """
        DESCRIBE tasks
        """
        
        cursor.execute(sql)
        results = cursor.fetchall()
        
        print(f"\ntasks表的字段:")
        for result in results:
            field, type, null, key, default, extra = result
            print(f"  {field}: {type}, null: {null}, key: {key}, default: {default}, extra: {extra}")
        
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
    query_tasks_structure()
