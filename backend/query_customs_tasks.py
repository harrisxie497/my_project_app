"""
查询CUSTOMS任务类型的任务
"""

import pymysql
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def query_customs_tasks():
    """查询CUSTOMS任务类型的任务"""
    print("=" * 100)
    print("查询CUSTOMS任务类型的任务")
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
        
        # 查询CUSTOMS任务类型的任务
        sql = """
        SELECT id, file_type, status
        FROM tasks
        WHERE file_type = 'CUSTOMS'
        ORDER BY created_at DESC
        LIMIT 5
        """
        
        cursor.execute(sql)
        results = cursor.fetchall()
        
        print(f"\n查询结果数量: {len(results)}")
        
        for result in results:
            task_id, file_type, status = result
            print(f"\n任务ID: {task_id}, 文件类型: {file_type}, 状态: {status}")
        
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
    query_customs_tasks()
