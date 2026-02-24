import sqlite3
import json

def check_columns_json():
    """检查columns_json内容"""
    connection = sqlite3.connect("test.db")
    
    try:
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        
        sql = """
        SELECT file_type, file_role, columns_json, header_row
        FROM file_definitions
        WHERE file_type = 'CUSTOMS' AND file_role = 'SOURCE'
        """
        cursor.execute(sql)
        result = cursor.fetchone()
        
        if result:
            print("=" * 100)
            print("file_definitions配置")
            print("=" * 100)
            print(f"file_type: {result['file_type']}")
            print(f"file_role: {result['file_role']}")
            print(f"header_row: {result['header_row']}")
            print(f"columns_json (原始): {result['columns_json']}")
            
            columns_json = json.loads(result['columns_json'])
            print(f"columns_json (解析后): {json.dumps(columns_json, indent=2, ensure_ascii=False)}")
        else:
            print("file_definitions配置不存在")
        
    finally:
        connection.close()

if __name__ == "__main__":
    check_columns_json()
