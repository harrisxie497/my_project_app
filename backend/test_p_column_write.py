"""
测试記事欄2（P列）写入情况
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
print("测试記事欄2（P列）配置和写入")
print("=" * 80)

try:
    connection = pymysql.connect(**MYSQL_CONFIG)
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    
    # 1. 检查P列配置
    print("\n【步骤1: 检查P列配置】")
    cursor.execute("""
        SELECT target_col, target_header, map_op, source_cols,
               rule_ref, rule_params_json
        FROM field_pipelines
        WHERE file_type = 'DELIVERY' AND target_col = 'P'
    """)
    p_config = cursor.fetchone()
    
    if p_config:
        print(f"  目标列: {p_config['target_col']}")
        print(f"  表头: {p_config['target_header']}")
        print(f"  操作: {p_config['map_op']}")
        print(f"  源列: {p_config['source_cols']}")
        print(f"  规则引用: {p_config['rule_ref']}")
        print(f"  规则参数: {p_config['rule_params_json']}")
        
        # 检查rule_params_json的值
        rule_params = p_config['rule_params_json']
        if isinstance(rule_params, str):
            rule_params = json.loads(rule_params)
        
        const_value = rule_params.get('policy_const', {}).get('value', '')
        print(f"\n  常量值: {const_value}")
        
        if const_value == '{{unique_code}}':
            print("  [OK] 常量值设置为 {{unique_code}}")
        else:
            print(f"  [FAIL] 常量值不是 {{unique_code}}")
    
    # 2. 检查DELIVERY任务的unique_code
    print("\n" + "=" * 80)
    print("【步骤2: 检查DELIVERY任务的unique_code】")
    cursor.execute("""
        SELECT id, unique_code, status
        FROM tasks
        WHERE file_type = 'DELIVERY'
        ORDER BY id DESC
        LIMIT 1
    """)
    task = cursor.fetchone()
    
    if task:
        print(f"  任务ID: {task['id']}")
        print(f"  unique_code: {task['unique_code']}")
        print(f"  状态: {task['status']}")
        
        # 模拟格式化
        unique_code = task['unique_code']
        if unique_code and len(unique_code) >= 8:
            formatted = unique_code[:8] + ' ' + unique_code[8:]
            print(f"\n  格式化模拟:")
            print(f"    原始值: {unique_code}")
            print(f"    格式化后: {formatted}")
            
            if formatted == "160-0327 0890":
                print("  [OK] 格式化正确")
            else:
                print(f"  [INFO] 格式化结果: {formatted}")
    
    # 3. 检查delivery_processor的日志
    print("\n" + "=" * 80)
    print("【步骤3: 检查delivery_processor格式化逻辑】")
    print("  代码位置: delivery_processor.py 第379-386行")
    print("  格式化逻辑: const_value[:8] + ' ' + const_value[8:]")
    print("\n  预期流程:")
    print("    1. const_value = '{{unique_code}}'")
    print("    2. 检测到特殊标记，const_value = '160-03270890'")
    print("    3. 格式化: const_value = '160-0327' + ' ' + '0890'")
    print("    4. const_value = '160-0327 0890'")
    print("    5. return set_constant('160-0327 0890')")
    
    cursor.close()
    connection.close()
    
    print("\n" + "=" * 80)
    print("测试完成")
    print("=" * 80)
    
    print("\n建议:")
    print("1. 检查任务执行日志，确认格式化逻辑是否被执行")
    print("2. 检查header_params中mawb_no的值是否正确传递")
    print("3. 检查result.xlsx文件中P列的实际值")
    print("4. 如果日志级别是INFO，尝试改为DEBUG查看详细信息")
    
except Exception as e:
    print(f"\n[FAIL] 错误: {str(e)}")
    import traceback
    traceback.print_exc()
