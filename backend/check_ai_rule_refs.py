import pymysql

conn = pymysql.connect(
    host='172.18.207.224',
    user='app',
    password='app123456',
    database='demo',
    charset='utf8mb4'
)

cursor = conn.cursor(pymysql.cursors.DictCursor)

# 查询所有AI规则的rule_ref
sql = """
SELECT rule_ref, target_header
FROM rule_definitions
WHERE rule_ref LIKE 'policy_ai%'
ORDER BY rule_ref
"""

cursor.execute(sql)
results = cursor.fetchall()

print("所有AI规则：")
print("=" * 100)
for row in results:
    print(f"rule_ref: {row['rule_ref']}, target_header: {row['target_header']}")

conn.close()
