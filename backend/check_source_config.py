import pymysql

def check_source_config():
    """检查SOURCE配置中的列定义"""
    print("=" * 100)
    print("检查SOURCE配置中的列定义")
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
        
        # 检查SOURCE配置
        sql = """
        SELECT col_name, col_header, col_type, file_role
        FROM file_definitions
        WHERE file_type = 'CUSTOMS' AND file_role = 'SOURCE'
        ORDER BY col_name
        """
        
        cursor.execute(sql)
        results = cursor.fetchall()
        
        print(f"\nSOURCE配置中的列定义:")
        for result in results:
            col_name, col_header, col_type, file_role = result
            print(f"  {col_name} ({col_header}): {col_type}")
        
        connection.close()
        
        print("\n" + "=" * 100)
        print("检查完成！")
        print("=" * 100)
        
    except Exception as e:
        print(f"错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    check_source_config()
