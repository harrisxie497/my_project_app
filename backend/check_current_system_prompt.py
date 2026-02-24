import pymysql

conn = pymysql.connect(
    host='172.18.207.224',
    user='app',
    password='app123456',
    database='demo',
    charset='utf8mb4'
)

cursor = conn.cursor(pymysql.cursors.DictCursor)

# 查询当前的系统提示词
sql = """
SELECT rule_ref, schema_json
FROM rule_definitions
WHERE rule_ref LIKE 'policy_ai%'
ORDER BY rule_ref
"""

cursor.execute(sql)
results = cursor.fetchall()

print("当前系统提示词：")
print("=" * 100)
for row in results:
    rule_ref = row['rule_ref']
    schema_json = row['schema_json']
    
    # 提取当前的system_prompt
    import json
    current_system_prompt = ""
    
    if schema_json:
        # 如果是字符串，先解析为字典
        if isinstance(schema_json, str):
            try:
                schema_json = json.loads(schema_json)
            except json.JSONDecodeError:
                pass
        
        # 提取 system_prompt
        if isinstance(schema_json, dict):
            configurable_params = schema_json.get('configurable_params', {})
            current_system_prompt = configurable_params.get('system_prompt', '')
    
    print(f"规则: {rule_ref}")
    print(f"当前系统提示词: {current_system_prompt[:200] if current_system_prompt else '无'}")
    print()

conn.close()
