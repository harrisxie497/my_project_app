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

# 查询所有AI规则的system_prompt
sql = """
SELECT rule_ref, schema_json
FROM rule_definitions
WHERE rule_ref LIKE 'policy_ai%'
ORDER BY rule_ref
"""

cursor.execute(sql)
results = cursor.fetchall()

print("所有AI规则的system_prompt：")
print("=" * 100)
for row in results:
    rule_ref = row['rule_ref']
    schema_json = row['schema_json']
    
    # 提取当前的system_prompt
    if schema_json and 'configurable_params' in schema_json:
        configurable_params = json.loads(schema_json)
        if 'system_prompt' in configurable_params:
            current_system_prompt = configurable_params['system_prompt']
        else:
            current_system_prompt = ""
    else:
        current_system_prompt = ""
    
    # 显示前200个字符
    if current_system_prompt:
        preview = current_system_prompt[:200]
        if len(current_system_prompt) > 200:
            preview += "..."
    else:
        preview = "无"
    
    print(f"规则: {rule_ref}")
    print(f"系统提示词: {preview}")
    print()

conn.close()
