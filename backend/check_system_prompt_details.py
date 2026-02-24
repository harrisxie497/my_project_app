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

# 查询每个AI规则的完整配置
sql = """
SELECT rule_ref, schema_json
FROM rule_definitions
WHERE rule_ref IN (
    'policy_ai_goods_en',
    'policy_ai_material_en',
    'policy_ai_text_ja_clean',
    'policy_ai_text_dress_clean',
    'policy_translate_from_targetcol_en_upper',
    'policy_translate_name_en_upper'
)
ORDER BY rule_ref
"""

cursor.execute(sql)
results = cursor.fetchall()

print("AI规则的系统提示词：")
print("=" * 100)
for row in results:
    rule_ref = row['rule_ref']
    schema_json = row['schema_json']
    
    # 提取当前的system_prompt
    current_system_prompt = ""
    if schema_json and 'configurable_params' in schema_json:
        configurable_params = json.loads(schema_json)
        if 'system_prompt' in configurable_params:
            current_system_prompt = configurable_params['system_prompt']
    
    # 反馈
    print(f"规则: {rule_ref}")
    print(f"当前系统提示词: {current_system_prompt if current_system_prompt else '无'}")
    print()

conn.close()
