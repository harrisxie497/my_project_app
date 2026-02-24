import pymysql

def check_sheet_name_in_file_definitions():
    """检查file_definitions中是否有sheet_name字段"""
    print("=" * 100)
    print("检查file_definitions中是否有sheet_name字段")
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
        
        # 查询file_definitions的表结构
        sql = """
        SHOW COLUMNS FROM file_definitions
        """
        
        cursor.execute(sql)
        results = cursor.fetchall()
        
        print(f"\nfile_definitions表结构:")
        for result in results:
            print(f"  {result}")
        
        # 查询CUSTOMS的配置
        sql = """
        SELECT file_type, file_role, sheet_name, header_row, data_start_row
        FROM file_definitions
        WHERE file_type = 'CUSTOMS'
        """
        
        cursor.execute(sql)
        results = cursor.fetchall()
        
        print(f"\nCUSTOMS配置:")
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
    check_sheet_name_in_file_definitions()
