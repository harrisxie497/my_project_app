import sqlite3

def check_file_definitions_table():
    """检查file_definitions表"""
    connection = sqlite3.connect("test.db")
    
    try:
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        
        # 查看表结构
        cursor.execute("PRAGMA table_info(file_definitions)")
        columns = cursor.fetchall()
        
        print("=" * 100)
        print("file_definitions表结构")
        print("=" * 100)
        for col in columns:
            print(f"列名: {col['name']}, 类型: {col['type']}")
        
        # 查看所有数据
        cursor.execute("SELECT * FROM file_definitions")
        results = cursor.fetchall()
        
        print("=" * 100)
        print("file_definitions表数据")
        print("=" * 100)
        for result in results:
            print(f"file_type: {result['file_type']}, file_role: {result['file_role']}, header_row: {result['header_row']}")
        
    finally:
        connection.close()

if __name__ == "__main__":
    check_file_definitions_table()
