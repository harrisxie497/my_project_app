import pymysql

def delete_and_reinsert():
    connection = pymysql.connect(
        host='172.18.207.224',
        user='root',
        password='root123456',
        database='demo',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
    
    try:
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM field_pipelines WHERE file_type = 'CUSTOMS'")
            deleted = cursor.rowcount
            print(f"已删除 {deleted} 条 CUSTOMS 记录")
            
            with open('init_customs_config.sql', 'r', encoding='utf-8') as f:
                sql_content = f.read()
                cursor.execute(sql_content)
            connection.commit()
            print("SQL文件重新执行成功！")
            
            cursor.execute("SELECT COUNT(*) as count FROM field_pipelines WHERE file_type = 'CUSTOMS'")
            result = cursor.fetchone()
            print(f"当前 CUSTOMS 记录数: {result['count']}")
            
    except Exception as e:
        print(f"执行失败: {e}")
        connection.rollback()
    finally:
        connection.close()

if __name__ == '__main__':
    delete_and_reinsert()
