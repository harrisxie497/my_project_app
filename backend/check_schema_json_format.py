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

# 查询一个规则的schema_json格式
sql = """
SELECT rule_ref, schema_json
FROM rule_definitions
WHERE rule_ref = 'policy_ai_goods_en'
LIMIT 1
"""

cursor.execute(sql)
results = cursor.fetchall()

print("schema_json格式示例：")
print("=" * 100)
for row in results:
    rule_ref = row['rule_ref']
    schema_json = row['schema_json']
    
    print(f"规则: {rule_ref}")
    print(f"schema_json: {schema_json}")
    print()

conn.close()
