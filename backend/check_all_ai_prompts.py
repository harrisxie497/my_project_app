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

# 查询所有AI规则的提示词
sql = '''
SELECT rule_ref, schema_json
FROM rule_definitions
WHERE rule_ref IN (
    'policy_ai_goods_en',
    'policy_ai_text_ja_clean',
    'policy_ai_text_dress_clean',
    'policy_translate_from_targetcol_en_upper',
    'policy_translate_name_en_upper'
)
ORDER BY rule_ref
'''
cursor.execute(sql)
results = cursor.fetchall()

print('=== 所有AI列的提示词配置 ===\n')
for rule_ref, schema_json in results:
    print(f'--- {rule_ref} ---')
    if schema_json:
        if isinstance(schema_json, str):
            schema_json = json.loads(schema_json)
        if isinstance(schema_json, str):
            schema_json = json.loads(schema_json)
        configurable_params = schema_json.get('configurable_params', {})
        system_prompt = configurable_params.get('system_prompt', '')
        if system_prompt:
            # 只显示前500个字符，避免太长
            preview = system_prompt[:500] + '...' if len(system_prompt) > 500 else system_prompt
            print(f'system_prompt:\n{preview}\n')
        else:
            print('system_prompt: 空')
    else:
        print('schema_json: 空')
    print()

cursor.close()
conn.close()
