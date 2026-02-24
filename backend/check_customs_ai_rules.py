import pymysql

conn = pymysql.connect(
    host='172.18.207.224',
    user='app',
    password='app123456',
    database='demo',
    charset='utf8mb4'
)

cursor = conn.cursor(pymysql.cursors.DictCursor)

# 查询CUSTOMS类型的AI规则
sql = """
SELECT fp.rule_ref, fp.target_col, fp.target_header, rd.rule_ref
FROM field_pipelines fp
LEFT JOIN rule_definitions rd ON fp.rule_ref = rd.rule_ref
WHERE fp.file_type = 'CUSTOMS' AND fp.rule_ref LIKE 'policy_ai%'
ORDER BY fp.target_col
"""

cursor.execute(sql)
results = cursor.fetchall()

print("CUSTOMS类型的AI规则：")
print("=" * 100)
for row in results:
    print(f"rule_ref: {row['rule_ref']}, target_col: {row['target_col']}, target_header: {row['target_header']}, rule_definitions.rule_ref: {row['rule_ref']}")

conn.close()
