"""
更新記事欄2（P列）配置，使用unique_code
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
print("更新記事欄2（P列）配置")
print("=" * 80)

try:
    connection = pymysql.connect(**MYSQL_CONFIG)
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    
    # 查询当前配置
    print("\n【更新前配置】")
    cursor.execute("""
        SELECT * FROM field_pipelines
        WHERE file_type = 'DELIVERY' AND target_col = 'P'
    """)
    old_config = cursor.fetchone()
    
    if old_config:
        print(f"  ID: {old_config['id']}")
        print(f"  目标列: {old_config['target_col']}")
        print(f"  表头: {old_config['target_header']}")
        print(f"  操作: {old_config['map_op']}")
        print(f"  规则引用: {old_config['rule_ref']}")
        print(f"  规则参数: {old_config['rule_params_json']}")
    else:
        print("  [FAIL] 未找到P列配置")
        cursor.close()
        connection.close()
        exit(1)
    
    # 更新配置
    print("\n【更新配置】")
    new_rule_params_json = json.dumps({
        "policy_const": {
            "value": "{{unique_code}}"
        }
    }, ensure_ascii=False)
    
    update_sql = """
        UPDATE field_pipelines
        SET map_op = 'CONST',
            field_type = 'RULE_FIX',
            rule_ref = '["policy_const"]',
            rule_params_json = %s,
            updated_at = NOW()
        WHERE file_type = 'DELIVERY' AND target_col = 'P'
    """
    
    cursor.execute(update_sql, (new_rule_params_json,))
    connection.commit()
    
    print(f"  [OK] P列配置已更新")
    print(f"    - 操作: CONST")
    print(f"    - 常量值: {{{{{{unique_code}}}}}}")
    print(f"    - 说明: 实际值将从header_params的mawb_no获取")
    
    # 查询更新后的配置
    print("\n【更新后配置】")
    cursor.execute("""
        SELECT * FROM field_pipelines
        WHERE file_type = 'DELIVERY' AND target_col = 'P'
    """)
    new_config = cursor.fetchone()
    
    if new_config:
        print(f"  ID: {new_config['id']}")
        print(f"  目标列: {new_config['target_col']}")
        print(f"  表头: {new_config['target_header']}")
        print(f"  操作: {new_config['map_op']}")
        print(f"  规则引用: {new_config['rule_ref']}")
        print(f"  规则参数: {new_config['rule_params_json']}")
        print(f"  更新时间: {new_config['updated_at']}")
    
    cursor.close()
    connection.close()
    
    print("\n" + "=" * 80)
    print("[OK] 記事欄2（P列）配置更新完成")
    print("=" * 80)
    
except Exception as e:
    print(f"\n[FAIL] 错误: {str(e)}")
    import traceback
    traceback.print_exc()
