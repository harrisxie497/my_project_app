"""
直接查询MySQL数据库验证配置
"""
import pymysql
import json

# 从config.py读取的MySQL配置
MYSQL_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': '123456',
    'database': 'excel_processor'
}

print("=" * 80)
print("MySQL配置信息")
print("=" * 80)
print(f"Host: {MYSQL_CONFIG['host']}")
print(f"Port: {MYSQL_CONFIG['port']}")
print(f"User: {MYSQL_CONFIG['user']}")
print(f"Database: {MYSQL_CONFIG['database']}")
print("")

try:
    # 连接数据库
    connection = pymysql.connect(**MYSQL_CONFIG)
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    
    # 查询SOURCE配置
    print("=" * 80)
    print("【SOURCE配置】")
    print("=" * 80)
    cursor.execute("""
        SELECT id, file_type, file_role, sheet_name, header_row, data_start_row, 
               enabled, columns_json, created_at, updated_at
        FROM file_definitions 
        WHERE file_type = 'DELIVERY' AND file_role = 'SOURCE'
    """)
    source_row = cursor.fetchone()
    
    if source_row:
        print(f"ID: {source_row['id']}")
        print(f"Sheet: {source_row['sheet_name']}")
        print(f"Header Row: {source_row['header_row']}")
        print(f"Data Start Row: {source_row['data_start_row']}")
        print(f"Enabled: {source_row['enabled']}")
        print(f"Updated At: {source_row['updated_at']}")
        
        columns = json.loads(source_row['columns_json']) if source_row['columns_json'] else []
        print(f"列数: {len(columns)}")
        print("\n列定义:")
        for i, col in enumerate(columns, 1):
            print(f"  {i}. {col['col']}: {col['header']}")
    else:
        print("[FAIL] 未找到SOURCE配置")
    
    # 查询OUTPUT配置
    print("\n" + "=" * 80)
    print("【OUTPUT配置】")
    print("=" * 80)
    cursor.execute("""
        SELECT id, file_type, file_role, sheet_name, header_row, data_start_row, 
               enabled, columns_json, created_at, updated_at
        FROM file_definitions 
        WHERE file_type = 'DELIVERY' AND file_role = 'OUTPUT'
    """)
    output_row = cursor.fetchone()
    
    if output_row:
        print(f"ID: {output_row['id']}")
        print(f"Sheet: {output_row['sheet_name']}")
        print(f"Header Row: {output_row['header_row']}")
        print(f"Data Start Row: {output_row['data_start_row']}")
        print(f"Enabled: {output_row['enabled']}")
        print(f"Updated At: {output_row['updated_at']}")
        
        columns = json.loads(output_row['columns_json']) if output_row['columns_json'] else []
        print(f"列数: {len(columns)}")
        print("\n列定义:")
        for i, col in enumerate(columns, 1):
            print(f"  {i}. {col['col']}: {col['header']}")
    else:
        print("[FAIL] 未找到OUTPUT配置")
    
    print("\n" + "=" * 80)
    print("[OK] 数据库查询完成")
    print("=" * 80)
    
    cursor.close()
    connection.close()
    
except Exception as e:
    print(f"\n[FAIL] 错误: {str(e)}")
    import traceback
    traceback.print_exc()
