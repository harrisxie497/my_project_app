import pymysql

conn = pymysql.connect(
    host='172.18.207.224',
    user='app',
    password='app123456',
    database='demo',
    charset='utf8mb4'
)

cursor = conn.cursor(pymysql.cursors.DictCursor)

# 查询品名和材质的配置
sql = """
SELECT target_col, target_header, rule_ref, rule_params_json
FROM field_pipelines
WHERE file_type = "CUSTOMS" AND target_col IN ('H', 'I')
ORDER BY target_col
"""

cursor.execute(sql)
results = cursor.fetchall()

print("品名和材质的配置：")
print("=" * 150)
for row in results:
    print(f"target_col: {row['target_col']}, target_header: {row['target_header']}, rule_ref: {row['rule_ref']}, rule_params_json: {row['rule_params_json']}")

conn.close()
