import pymysql

def check_existing_data():
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
            cursor.execute("SELECT * FROM field_pipelines LIMIT 1")
            result = cursor.fetchone()
            if result:
                print("现有数据示例:")
                for key, value in result.items():
                    print(f"  {key}: {value}")
            else:
                print("表中没有数据")
                
    except Exception as e:
        print(f"查询失败: {e}")
    finally:
        connection.close()

if __name__ == '__main__':
    check_existing_data()
