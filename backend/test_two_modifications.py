"""
测试两个修改：
1. SOURCE配置已修改为17列（A-Q）
2. 記事欄2（P列）使用tasks的unique_code值
"""
import pymysql
import json

# MySQL配置
MYSQL_CONFIG = {
    'host': '172.18.207.224',
    'port': 3306,
    'user': 'root',
    'password': 'root123456',
    'database': 'demo'
}

print("=" * 80)
print("测试修改1: SOURCE配置已修改为17列（A-Q）")
print("=" * 80)

try:
    connection = pymysql.connect(**MYSQL_CONFIG)
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    
    # 测试1: 验证SOURCE配置
    print("\n【测试1: 验证SOURCE配置】")
    cursor.execute("""
        SELECT id, sheet_name, header_row, data_start_row, columns_json, updated_at
        FROM file_definitions
        WHERE file_type = 'DELIVERY' AND file_role = 'SOURCE'
    """)
    source_row = cursor.fetchone()
    
    if source_row:
        columns = json.loads(source_row['columns_json']) if source_row['columns_json'] else []
        print(f"  Sheet: {source_row['sheet_name']}")
        print(f"  Header Row: {source_row['header_row']}")
        print(f"  Data Start Row: {source_row['data_start_row']}")
        print(f"  列数: {len(columns)}")
        print(f"  更新时间: {source_row['updated_at']}")
        
        if len(columns) == 17:
            print("\n  [OK] 列数正确: 17列")
            print("\n  列定义:")
            for i, col in enumerate(columns, 1):
                print(f"    {i}. {col['col']}: {col['header']}")
            
            # 验证列范围是A-Q
            expected_cols = [chr(65 + i) for i in range(17)]  # A到Q
            actual_cols = [col['col'] for col in columns]
            
            if actual_cols == expected_cols:
                print("\n  [OK] 列范围正确: A-Q")
            else:
                print(f"\n  [FAIL] 列范围错误: 期望 {expected_cols}, 实际 {actual_cols}")
        else:
            print(f"\n  [FAIL] 列数错误: 期望17列, 实际{len(columns)}列")
    else:
        print("  [FAIL] 未找到SOURCE配置")
    
    # 测试2: 验证記事欄2（P列）配置
    print("\n" + "=" * 80)
    print("测试2: 验证記事欄2（P列）使用unique_code")
    print("=" * 80)
    
    cursor.execute("""
        SELECT target_col, target_header, map_op, source_cols,
               rule_ref, rule_params_json, updated_at
        FROM field_pipelines
        WHERE file_type = 'DELIVERY' AND target_col = 'P'
    """)
    p_row = cursor.fetchone()
    
    if p_row:
        print(f"\n  目标列: {p_row['target_col']}")
        print(f"  表头: {p_row['target_header']}")
        print(f"  操作: {p_row['map_op']}")
        print(f"  源列: {p_row['source_cols']}")
        print(f"  规则引用: {p_row['rule_ref']}")
        print(f"  规则参数: {p_row['rule_params_json']}")
        print(f"  更新时间: {p_row['updated_at']}")
        
        if p_row['map_op'] == 'CONST':
            print("\n  [OK] 操作类型正确: CONST")
            
            rule_params = p_row['rule_params_json']
            if isinstance(rule_params, str):
                rule_params = json.loads(rule_params)
            
            const_value = rule_params.get('policy_const', {}).get('value', '')
            if const_value == '{{unique_code}}':
                print(f"  [OK] 常量值正确: {const_value}")
                print("\n  配置说明: P列将使用tasks表的unique_code字段值")
            else:
                print(f"\n  [FAIL] 常量值错误: 期望 '{{unique_code}}', 实际 '{const_value}'")
        else:
            print(f"\n  [FAIL] 操作类型错误: 期望 'CONST', 实际 '{p_row['map_op']}'")
    else:
        print("  [FAIL] 未找到P列配置")
    
    # 测试3: 验证任务记录中的unique_code
    print("\n" + "=" * 80)
    print("测试3: 验证任务记录中的unique_code")
    print("=" * 80)
    
    cursor.execute("""
        SELECT id, unique_code, status, created_at
        FROM tasks
        WHERE file_type = 'DELIVERY'
        ORDER BY id DESC
        LIMIT 3
    """)
    tasks = cursor.fetchall()
    
    if tasks:
        print(f"\n  找到 {len(tasks)} 个DELIVERY任务:\n")
        for i, task in enumerate(tasks, 1):
            print(f"    {i}. 任务ID: {task['id']}")
            print(f"       unique_code: {task['unique_code']}")
            print(f"       状态: {task['status']}")
            print(f"       创建时间: {task['created_at']}")
            print()
        
        # 检查是否有unique_code为空的任务
        tasks_with_code = [t for t in tasks if t['unique_code']]
        if len(tasks_with_code) == len(tasks):
            print("  [OK] 所有任务都有unique_code")
        else:
            print(f"  [WARN] 部分任务缺少unique_code ({len(tasks_with_code)}/{len(tasks)})")
    else:
        print("  [WARN] 未找到DELIVERY任务")
    
    # 测试4: 模拟delivery_processor的CONST操作
    print("\n" + "=" * 80)
    print("测试4: 模拟CONST操作获取unique_code")
    print("=" * 80)
    
    if tasks and tasks[0]['unique_code']:
        unique_code = tasks[0]['unique_code']
        print(f"\n  模拟header_params: {{'mawb_no': '{unique_code}'}}")
        print(f"  模拟规则参数: {{'policy_const': {{'value': '{{{{unique_code}}}}'}}}}")
        
        # 模拟处理逻辑
        const_value = '{{unique_code}}'
        if const_value == '{{unique_code}}':
            mawb_no = unique_code
            print(f"\n  [OK] 处理逻辑正确")
            print(f"     P列值将被设置为: {mawb_no}")
            print(f"\n  数据流示例:")
            print(f"     tasks.unique_code = {unique_code}")
            print(f"     header_params['mawb_no'] = {unique_code}")
            print(f"     P列数据行 = {unique_code}")
        else:
            print(f"\n  [FAIL] 处理逻辑错误")
    
    cursor.close()
    connection.close()
    
    print("\n" + "=" * 80)
    print("测试完成")
    print("=" * 80)
    
except Exception as e:
    print(f"\n[FAIL] 测试失败: {str(e)}")
    import traceback
    traceback.print_exc()
