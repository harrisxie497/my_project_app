import pymysql

def check_columns_json_type():
    """检查columns_json字段类型"""
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
            cursor.execute("SELECT columns_json FROM file_definitions WHERE file_type = 'CUSTOMS' AND file_role = 'SOURCE'")
            result = cursor.fetchone()
            
            if result:
                columns_json_value = result[0]
                print("=" * 100)
                print("columns_json字段检查")
                print("=" * 100)
                print(f"columns_json类型: {type(columns_json_value)}")
                print(f"columns_json值: {columns_json_value}")
                print(f"columns_json长度: {len(str(columns_json_value))}")
            else:
                print("没有找到数据")
        
    finally:
        connection.close()

if __name__ == "__main__":
    check_columns_json_type()
