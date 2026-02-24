import pymysql

conn = pymysql.connect(
    host='172.18.207.224',
    user='app',
    password='app123456',
    database='demo',
    charset='utf8mb4'
)

cursor = conn.cursor(pymysql.cursors.DictCursor)

# 查询DELIVERY类型的所有列
sql = """
SELECT file_type, target_col, target_header, field_type, rule_ref, rule_params_json
FROM field_pipelines
WHERE file_type = "DELIVERY"
ORDER BY target_col
"""

cursor.execute(sql)
results = cursor.fetchall()

print("DELIVERY类型的所有列：")
print("=" * 150)
for row in results:
    print(f"file_type: {row['file_type']}, target_col: {row['target_col']}, target_header: {row['target_header']}, field_type: {row['field_type']}, rule_ref: {row['rule_ref']}, rule_params_json: {row['rule_params_json']}")

conn.close()
