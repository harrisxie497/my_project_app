import pymysql

def verify_data():
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
            cursor.execute("SELECT COUNT(*) as count FROM field_pipelines WHERE file_type = 'CUSTOMS'")
            result = cursor.fetchone()
            print(f"CUSTOMS 类型的记录数: {result['count']}")
            
            cursor.execute("SELECT * FROM field_pipelines WHERE file_type = 'CUSTOMS' ORDER BY `order`")
            records = cursor.fetchall()
            print("\n前5条记录:")
            for i, record in enumerate(records[:5], 1):
                print(f"{i}. {record['target_col']} - {record['target_header']} - {record['map_op']}")
                
    except Exception as e:
        print(f"查询失败: {e}")
    finally:
        connection.close()

if __name__ == '__main__':
    verify_data()
