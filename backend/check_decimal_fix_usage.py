import pymysql

conn = pymysql.connect(
    host='172.18.207.224',
    user='app',
    password='app123456',
    database='demo',
    charset='utf8mb4'
)

cursor = conn.cursor(pymysql.cursors.DictCursor)

# 查询所有使用policy_ai_decimal_fix的列
sql = """
SELECT file_type, target_col, target_header, field_type, rule_ref
FROM field_pipelines
WHERE JSON_CONTAINS(rule_ref, '"policy_ai_decimal_fix"')
ORDER BY file_type, target_col
"""

cursor.execute(sql)
results = cursor.fetchall()

print("使用policy_ai_decimal_fix的列：")
print("=" * 150)
if results:
    for row in results:
        print(f"file_type: {row['file_type']}, target_col: {row['target_col']}, target_header: {row['target_header']}, field_type: {row['field_type']}, rule_ref: {row['rule_ref']}")
else:
    print("没有找到使用policy_ai_decimal_fix的列")

conn.close()
