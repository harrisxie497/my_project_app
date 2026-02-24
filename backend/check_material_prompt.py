import pymysql
import json

conn = pymysql.connect(
    host='172.18.207.224',
    port=3306,
    user='app',
    password='app123456',
    database='demo',
    charset='utf8mb4'
)
cursor = conn.cursor()

# 查询 rule_definitions 表
sql = '''
SELECT rule_ref, schema_json
FROM rule_definitions
WHERE rule_ref = %s
'''
cursor.execute(sql, ('policy_ai_material_en',))
result = cursor.fetchone()

if result:
    rule_ref, schema_json = result
    print('=== rule_definitions 表 ===')
    print(f'rule_ref: {rule_ref}')
    if schema_json:
        if isinstance(schema_json, str):
            schema_json = json.loads(schema_json)
        if isinstance(schema_json, str):
            schema_json = json.loads(schema_json)
        print(f'schema_json: {json.dumps(schema_json, ensure_ascii=False, indent=2)}')
        configurable_params = schema_json.get('configurable_params', {})
        system_prompt = configurable_params.get('system_prompt', '')
        print(f'\nsystem_prompt: {system_prompt}')
    else:
        print('schema_json: None')
else:
    print('未找到该规则')

cursor.close()
conn.close()
