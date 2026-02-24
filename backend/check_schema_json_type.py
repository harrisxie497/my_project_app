import pymysql
import json

conn = pymysql.connect(
    host='172.18.207.224',
    user='app',
    password='app123456',
    database='demo',
    charset='utf8mb4'
)

cursor = conn.cursor(pymysql.cursors.DictCursor)

# 查询Y列的schema_json
cursor.execute('''
    SELECT 
        schema_json
    FROM rule_definitions
    WHERE rule_ref = 'policy_ai_text_dress_clean'
''')

results = cursor.fetchall()

for row in results:
    schema_json = row['schema_json']
    print('=' * 100)
    print(f'schema_json类型: {type(schema_json)}')
    print(f'schema_json: {schema_json}')
    
    # 尝试解析JSON
    if isinstance(schema_json, str):
        try:
            schema_json_dict = json.loads(schema_json)
            print(f'JSON解析成功')
            print(f'schema_json_dict类型: {type(schema_json_dict)}')
            print(f'configurable_params: {schema_json_dict.get("configurable_params", {})}')
        except json.JSONDecodeError as e:
            print(f'JSON解析失败: {e}')
    elif isinstance(schema_json, dict):
        print(f'schema_json已经是字典')
        print(f'configurable_params: {schema_json.get("configurable_params", {})}')
    print()

conn.close()
