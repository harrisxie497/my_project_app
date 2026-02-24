"""
查询SQLite数据库中的配置
"""
import sqlite3
import json

DB_PATH = "./test.db"

print("=" * 80)
print("SQLite数据库配置信息")
print("=" * 80)
print(f"数据库路径: {DB_PATH}")
print("")

try:
    # 连接数据库
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
    
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
        print(f"ID: {source_row[0]}")
        print(f"File Type: {source_row[1]}")
        print(f"File Role: {source_row[2]}")
        print(f"Sheet: {source_row[3]}")
        print(f"Header Row: {source_row[4]}")
        print(f"Data Start Row: {source_row[5]}")
        print(f"Enabled: {source_row[6]}")
        print(f"Created At: {source_row[8]}")
        print(f"Updated At: {source_row[9]}")
        
        columns = json.loads(source_row[7]) if source_row[7] else []
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
        print(f"ID: {output_row[0]}")
        print(f"File Type: {output_row[1]}")
        print(f"File Role: {output_row[2]}")
        print(f"Sheet: {output_row[3]}")
        print(f"Header Row: {output_row[4]}")
        print(f"Data Start Row: {output_row[5]}")
        print(f"Enabled: {output_row[6]}")
        print(f"Created At: {output_row[8]}")
        print(f"Updated At: {output_row[9]}")
        
        columns = json.loads(output_row[7]) if output_row[7] else []
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
