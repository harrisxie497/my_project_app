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

# 查询所有AI规则的定义
sql = """
SELECT rule_ref, schema_json
FROM rule_definitions
WHERE rule_ref IN (
    'policy_ai_goods_en',
    'policy_ai_material_en',
    'policy_translate_name_en_upper',
    'policy_translate_from_targetcol_en_upper',
    'policy_ai_text_ja_clean',
    'policy_ai_text_dress_clean'
)
"""

cursor.execute(sql)
results = cursor.fetchall()

print("rule_definitions 表中的system_prompt：")
print("=" * 150)
for row in results:
    rule_ref = row['rule_ref']
    schema_json = row['schema_json']
    
    # 解析schema_json
    if isinstance(schema_json, str):
        try:
            # 第一次解析
            schema_json = json.loads(schema_json)
            # 如果解析后仍然是字符串，则进行第二次解析
            if isinstance(schema_json, str):
                schema_json = json.loads(schema_json)
        except json.JSONDecodeError as e:
            print(f"解析schema_json失败: {e}")
            continue
    
    configurable_params = schema_json.get('configurable_params', {}) if isinstance(schema_json, dict) else {}
    system_prompt = configurable_params.get('system_prompt', '') if isinstance(configurable_params, dict) else ''
    
    print(f"rule_ref: {rule_ref}")
    print(f"system_prompt: {system_prompt}")
    print()

conn.close()
