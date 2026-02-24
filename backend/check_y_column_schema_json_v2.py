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
        fp.target_col,
        fp.target_header,
        fp.rule_ref,
        rd.schema_json
    FROM field_pipelines fp
    LEFT JOIN rule_definitions rd ON fp.rule_ref LIKE CONCAT('%', rd.rule_ref, '%')
    WHERE fp.target_col = 'Y' AND fp.file_type = 'CUSTOMS'
''')

results = cursor.fetchall()

for row in results:
    print('=' * 100)
    print(f'列: {row["target_col"]} - {row["target_header"]}')
    print('=' * 100)
    print(f'rule_ref: {row["rule_ref"]}')
    print(f'schema_json类型: {type(row["schema_json"])}')
    print(f'schema_json: {row["schema_json"]}')
    
    # 尝试解析JSON
    if isinstance(row["schema_json"], str):
        try:
            schema_json_dict = json.loads(row["schema_json"])
            print(f'JSON解析成功: {schema_json_dict}')
            print(f'configurable_params: {schema_json_dict.get("configurable_params", {})}')
            print(f'system_prompt: {schema_json_dict.get("configurable_params", {}).get("system_prompt", "")}')
        except json.JSONDecodeError as e:
            print(f'JSON解析失败: {e}')
    elif isinstance(row["schema_json"], dict):
        print(f'schema_json已经是字典: {row["schema_json"]}')
        print(f'configurable_params: {row["schema_json"].get("configurable_params", {})}')
        print(f'system_prompt: {row["schema_json"].get("configurable_params", {}).get("system_prompt", "")}')
    print()

conn.close()
