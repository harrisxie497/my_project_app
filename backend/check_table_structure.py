import pymysql

def check_table_structure():
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
            cursor.execute("DESCRIBE field_pipelines")
            columns = cursor.fetchall()
            print("field_pipelines 表结构:")
            for i, col in enumerate(columns, 1):
                print(f"{i}. {col['Field']} - {col['Type']}")
            print(f"\n总列数: {len(columns)}")
            
    except Exception as e:
        print(f"查询失败: {e}")
    finally:
        connection.close()

if __name__ == '__main__':
    check_table_structure()
