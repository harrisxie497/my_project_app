import pymysql

conn = pymysql.connect(
    host='172.18.207.224',
    user='app',
    password='app123456',
    database='demo',
    charset='utf8mb4'
)

cursor = conn.cursor(pymysql.cursors.DictCursor)

# 查询一个规则的 schema_json
sql = """
SELECT rule_ref, schema_json
FROM rule_definitions
WHERE rule_ref = 'policy_ai_goods_en'
"""

cursor.execute(sql)
result = cursor.fetchone()

print("规则:", result['rule_ref'])
print("\nschema_json 类型:", type(result['schema_json']))
print("\nschema_json 内容:")
print(result['schema_json'])

# 如果是字符串，尝试解析
if isinstance(result['schema_json'], str):
    import json
    parsed = json.loads(result['schema_json'])
    print("\n解析后的类型:", type(parsed))
    print("\n解析后的内容:")
    print(json.dumps(parsed, indent=2, ensure_ascii=False))
    
    # 查看 configurable_params
    configurable_params = parsed.get('configurable_params', {})
    print("\nconfigurable_params:")
    print(json.dumps(configurable_params, indent=2, ensure_ascii=False))
    
    print("\nsystem_prompt:")
    print(configurable_params.get('system_prompt', '无'))
elif isinstance(result['schema_json'], dict):
    print("\n已经是字典类型")
    configurable_params = result['schema_json'].get('configurable_params', {})
    print("\nconfigurable_params:")
    print(configurable_params)
    
    print("\nsystem_prompt:")
    print(configurable_params.get('system_prompt', '无'))

conn.close()
