import pymysql

def check_file_definitions_structure():
    """检查file_definitions表的结构"""
    print("=" * 100)
    print("检查file_definitions表的结构")
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
        
        # 查看表结构
        sql = "DESCRIBE file_definitions"
        cursor.execute(sql)
        results = cursor.fetchall()
        
        print(f"\nfile_definitions表结构:")
        for result in results:
            print(f"  {result}")
        
        # 查看SOURCE配置
        sql = """
        SELECT * FROM file_definitions
        WHERE file_type = 'CUSTOMS' AND file_role = 'SOURCE'
        ORDER BY id
        """
        
        cursor.execute(sql)
        results = cursor.fetchall()
        
        print(f"\nSOURCE配置:")
        for result in results:
            print(f"  {result}")
        
        connection.close()
        
        print("\n" + "=" * 100)
        print("检查完成！")
        print("=" * 100)
        
    except Exception as e:
        print(f"错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    check_file_definitions_structure()
