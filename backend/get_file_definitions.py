import sqlite3

def get_file_definitions():
    """获取file_definitions配置"""
    connection = sqlite3.connect("test.db")
    
    try:
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        
        sql = """
        SELECT file_type, file_role, sheet_name, header_row, data_start_row, columns_json, enabled
        FROM file_definitions
        WHERE enabled = 1
        """
        cursor.execute(sql)
        results = cursor.fetchall()
        
        print("=" * 100)
        print("FILE_DEFINITIONS 配置列表")
        print("=" * 100)
        
        for row in results:
            print(f"\n文件类型: {row['file_type']}")
            print(f"  角色: {row['file_role']}")
            print(f"  工作表名称: {row['sheet_name']}")
            print(f"  表头行: {row['header_row']}")
            print(f"  数据开始行: {row['data_start_row']}")
            print(f"  列定义: {row['columns_json']}")
            print(f"  启用: {row['enabled']}")
            print("-" * 100)
        
        print(f"\n总计: {len(results)} 个文件定义配置")
        
    finally:
        connection.close()

if __name__ == "__main__":
    get_file_definitions()
