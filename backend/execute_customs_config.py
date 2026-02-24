import pymysql

def execute_sql_file():
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
            with open('init_customs_config.sql', 'r', encoding='utf-8') as f:
                sql_content = f.read()
                cursor.execute(sql_content)
            connection.commit()
            print("SQL文件执行成功！")
            
    except Exception as e:
        print(f"执行失败: {e}")
        connection.rollback()
    finally:
        connection.close()

if __name__ == '__main__':
    execute_sql_file()
