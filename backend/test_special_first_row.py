"""
测试特殊第一行逻辑：
- DELIVERY: 不应该有特殊第一行，表头在第1行，数据从第2行开始
- CUSTOMS: 应该有特殊第一行，表头在第2行，数据从第3行开始
"""
import pymysql

# MySQL配置
MYSQL_CONFIG = {
    'host': '172.18.207.224',
    'port': 3306,
    'user': 'root',
    'password': 'root123456',
    'database': 'demo'
}

print("=" * 80)
print("测试特殊第一行逻辑")
print("=" * 80)

try:
    connection = pymysql.connect(**MYSQL_CONFIG)
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    
    # 测试1: 查询DELIVERY的SOURCE配置
    print("\n【测试1: DELIVERY的SOURCE配置】")
    cursor.execute("""
        SELECT file_role, sheet_name, header_row, data_start_row
        FROM file_definitions
        WHERE file_type = 'DELIVERY' AND file_role = 'SOURCE'
    """)
    delivery_source = cursor.fetchone()
    
    if delivery_source:
        print(f"  File Role: {delivery_source['file_role']}")
        print(f"  Sheet: {delivery_source['sheet_name']}")
        print(f"  Header Row: {delivery_source['header_row']}")
        print(f"  Data Start Row: {delivery_source['data_start_row']}")
        
        if delivery_source['header_row'] == 1 and delivery_source['data_start_row'] == 2:
            print("\n  [OK] DELIVERY配置正确: 表头在第1行，数据从第2行开始")
            print("  [OK] 不需要特殊第一行")
        else:
            print(f"\n  [FAIL] DELIVERY配置错误")
    
    # 测试2: 查询DELIVERY的OUTPUT配置
    print("\n" + "=" * 80)
    print("【测试2: DELIVERY的OUTPUT配置】")
    cursor.execute("""
        SELECT file_role, sheet_name, header_row, data_start_row
        FROM file_definitions
        WHERE file_type = 'DELIVERY' AND file_role = 'OUTPUT'
    """)
    delivery_output = cursor.fetchone()
    
    if delivery_output:
        print(f"  File Role: {delivery_output['file_role']}")
        print(f"  Sheet: {delivery_output['sheet_name']}")
        print(f"  Header Row: {delivery_output['header_row']}")
        print(f"  Data Start Row: {delivery_output['data_start_row']}")
        
        if delivery_output['header_row'] == 1 and delivery_output['data_start_row'] == 2:
            print("\n  [OK] DELIVERY OUTPUT配置正确")
            print("  [OK] 不需要特殊第一行")
        else:
            print(f"\n  [FAIL] DELIVERY OUTPUT配置错误")
    
    # 测试3: 查询CUSTOMS的配置
    print("\n" + "=" * 80)
    print("【测试3: CUSTOMS的配置（对比）】")
    cursor.execute("""
        SELECT file_role, sheet_name, header_row, data_start_row
        FROM file_definitions
        WHERE file_type = 'CUSTOMS' AND file_role = 'OUTPUT'
        LIMIT 1
    """)
    customs_output = cursor.fetchone()
    
    if customs_output:
        print(f"  File Role: {customs_output['file_role']}")
        print(f"  Sheet: {customs_output['sheet_name']}")
        print(f"  Header Row: {customs_output['header_row']}")
        print(f"  Data Start Row: {customs_output['data_start_row']}")
        
        if customs_output['header_row'] == 2 and customs_output['data_start_row'] == 3:
            print("\n  [OK] CUSTOMS配置正确: 表头在第2行，数据从第3行开始")
            print("  [OK] 需要特殊第一行")
        else:
            print(f"\n  [WARN] CUSTOMS配置格式: header_row={customs_output['header_row']}, data_start_row={customs_output['data_start_row']}")
    
    # 测试4: 模拟Excel写入
    print("\n" + "=" * 80)
    print("【测试4: 模拟Excel写入结构】")
    
    print("\nDELIVERY类型的Excel结构:")
    print("  第1行: 表头 (headers)")
    print("  第2行: 数据行1")
    print("  第3行: 数据行2")
    print("  ...")
    print("\nCUSTOMS类型的Excel结构:")
    print("  第1行: 特殊第一行 (special_first_row)")
    print("  第2行: 表头 (headers)")
    print("  第3行: 数据行1")
    print("  第4行: 数据行2")
    print("  ...")
    
    print("\n" + "=" * 80)
    print("测试完成")
    print("=" * 80)
    
    cursor.close()
    connection.close()
    
except Exception as e:
    print(f"\n[FAIL] 错误: {str(e)}")
    import traceback
    traceback.print_exc()
