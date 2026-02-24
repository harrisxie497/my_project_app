import pymysql

conn = pymysql.connect(
    host='172.18.207.224',
    user='app',
    password='app123456',
    database='demo',
    charset='utf8mb4'
)

cursor = conn.cursor(pymysql.cursors.DictCursor)

# 查询所有AI规则的handler
sql = """
SELECT rule_ref, schema_json
FROM rule_definitions
WHERE rule_ref IN (
    'policy_ai_goods_en',
    'policy_ai_material_en',
    'policy_ai_text_dress_clean',
    'policy_ai_text_ja_clean',
    'policy_translate_from_targetcol_en_upper',
    'policy_translate_name_en_upper'
)
"""

cursor.execute(sql)
results = cursor.fetchall()

print("AI规则的handler：")
print("=" * 150)
for row in results:
    rule_ref = row['rule_ref']
    schema_json = row['schema_json']
    
    # 解析schema_json
    if isinstance(schema_json, str):
        import json
        try:
            schema_json = json.loads(schema_json)
            if isinstance(schema_json, str):
                schema_json = json.loads(schema_json)
        except json.JSONDecodeError as e:
            print(f"解析schema_json失败: {e}")
            continue
    
    handler = schema_json.get('handler', '') if isinstance(schema_json, dict) else ''
    print(f"rule_ref: {rule_ref}, handler: {handler}")

conn.close()
