"""
更新MySQL数据库中的DELIVERY配置
"""
import pymysql
import json

# 用户提供的MySQL配置
MYSQL_CONFIG = {
    'host': '172.18.207.224',
    'port': 3306,
    'user': 'root',
    'password': 'root123456',
    'database': 'demo'
}

# 新的SOURCE配置（17列 A-Q）
NEW_SOURCE_COLUMNS = [
    {"col": "A", "header": "お客様管理番号"},
    {"col": "B", "header": "佐川問合せ番号HAWB"},
    {"col": "C", "header": "配達指定日"},
    {"col": "D", "header": "時間帯指定"},
    {"col": "E", "header": "貨物個数"},
    {"col": "F", "header": "お届け先人名"},
    {"col": "G", "header": "お届け先住所"},
    {"col": "H", "header": "お届け先電話"},
    {"col": "I", "header": "お届け先郵便"},
    {"col": "J", "header": "依頼主"},
    {"col": "K", "header": "依頼主住所"},
    {"col": "L", "header": "依頼主郵便番号"},
    {"col": "M", "header": "依頼主電話"},
    {"col": "N", "header": "佐川顧客コード（固定）"},
    {"col": "O", "header": "記事欄2（品名）"},
    {"col": "P", "header": "記事欄2"},
    {"col": "Q", "header": "記事欄3"}
]

print("=" * 80)
print("连接MySQL数据库")
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
    print("[OK] 数据库连接成功\n")
    
    # 查询当前SOURCE配置
    print("=" * 80)
    print("【更新前SOURCE配置】")
    print("=" * 80)
    cursor.execute("""
        SELECT id, file_type, file_role, sheet_name, header_row, data_start_row,
               enabled, columns_json, updated_at
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
        
        old_columns = json.loads(source_row['columns_json']) if source_row['columns_json'] else []
        print(f"当前列数: {len(old_columns)}")
        print("\n当前列定义:")
        for i, col in enumerate(old_columns, 1):
            print(f"  {i}. {col['col']}: {col['header']}")
    else:
        print("[FAIL] 未找到SOURCE配置")
        cursor.close()
        connection.close()
        exit(1)
    
    # 更新SOURCE配置
    print("\n" + "=" * 80)
    print("【更新SOURCE配置】")
    print("=" * 80)
    
    new_columns_json = json.dumps(NEW_SOURCE_COLUMNS, ensure_ascii=False)
    
    update_sql = """
        UPDATE file_definitions
        SET columns_json = %s,
            sheet_name = 'Speedy',
            updated_at = NOW()
        WHERE file_type = 'DELIVERY' AND file_role = 'SOURCE'
    """
    
    cursor.execute(update_sql, (new_columns_json,))
    connection.commit()
    
    print(f"[OK] SOURCE配置已更新")
    print(f"    - 新列数: {len(NEW_SOURCE_COLUMNS)}")
    print(f"    - Sheet: Speedy")
    
    # 查询更新后的配置
    print("\n" + "=" * 80)
    print("【更新后SOURCE配置】")
    print("=" * 80)
    cursor.execute("""
        SELECT id, file_type, file_role, sheet_name, header_row, data_start_row,
               enabled, columns_json, updated_at
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
        
        new_columns = json.loads(source_row['columns_json']) if source_row['columns_json'] else []
        print(f"新列数: {len(new_columns)}")
        print("\n新列定义:")
        for i, col in enumerate(new_columns, 1):
            print(f"  {i}. {col['col']}: {col['header']}")
    
    # 查询OUTPUT配置（不做修改）
    print("\n" + "=" * 80)
    print("【OUTPUT配置】(未修改)")
    print("=" * 80)
    cursor.execute("""
        SELECT id, sheet_name, header_row, data_start_row, enabled, columns_json, updated_at
        FROM file_definitions
        WHERE file_type = 'DELIVERY' AND file_role = 'OUTPUT'
    """)
    output_row = cursor.fetchone()
    
    if output_row:
        print(f"ID: {output_row['id']}")
        print(f"Sheet: {output_row['sheet_name']}")
        print(f"列数: {len(json.loads(output_row['columns_json']))}")
    
    print("\n" + "=" * 80)
    print("[OK] MySQL数据库配置更新完成")
    print("=" * 80)
    
    cursor.close()
    connection.close()
    
except Exception as e:
    print(f"\n[FAIL] 错误: {str(e)}")
    import traceback
    traceback.print_exc()
