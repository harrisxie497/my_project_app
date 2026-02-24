import sqlite3

def check_file_definitions_columns():
    """检查file_definitions的列配置"""
    connection = sqlite3.connect("test.db")
    
    try:
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        
        sql = """
        SELECT id, file_type, file_role, sheet_name, columns_json
        FROM file_definitions
        WHERE enabled = 1
        """
        cursor.execute(sql)
        results = cursor.fetchall()
        
        print("=" * 100)
        print("FILE_DEFINITIONS 列配置检查")
        print("=" * 100)
        
        for row in results:
            print(f"\nID: {row['id']}")
            print(f"  文件类型: {row['file_type']}")
            print(f"  角色: {row['file_role']}")
            print(f"  工作表名称: {row['sheet_name']}")
            print(f"  列定义: {row['columns_json']}")
            
            if row['columns_json']:
                import json
                columns = json.loads(row['columns_json'])
                print(f"  列数量: {len(columns)}")
                print(f"  列列表: {[col.get('col') for col in columns]}")
                print(f"  最后几列: {[col.get('col') for col in columns[-5:]]}")
            print("-" * 100)
        
    finally:
        connection.close()

if __name__ == "__main__":
    check_file_definitions_columns()
