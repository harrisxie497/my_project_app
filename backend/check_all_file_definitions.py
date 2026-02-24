import pymysql

def check_all_file_definitions():
    """检查所有file_definitions"""
    connection = pymysql.connect(
        host='172.18.207.224',
        port=3306,
        user='app',
        password='app123456',
        database='demo',
        charset='utf8mb4'
    )
    
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM file_definitions")
            results = cursor.fetchall()
            
            print("=" * 100)
            print("所有file_definitions数据")
            print("=" * 100)
            for result in results:
                print(f"file_type: {result[1]}, file_role: {result[2]}, header_row: {result[4]}")
                print(f"  所有列: {result}")
                print(f"  columns_json索引5的值: {result[5]}")
                print(f"  columns_json类型: {type(result[5])}")
        
    finally:
        connection.close()

if __name__ == "__main__":
    check_all_file_definitions()
