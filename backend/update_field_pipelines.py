import pymysql

conn = pymysql.connect(
    host='172.18.207.224',
    user='app',
    password='app123456',
    database='demo',
    charset='utf8mb4'
)

cursor = conn.cursor()

# 修改J列的rule_params_json
sql = """
UPDATE field_pipelines
SET rule_params_json = '{"policy_translate_name_en_upper": {}}'
WHERE file_type = 'CUSTOMS' AND target_col = 'J'
"""

cursor.execute(sql)
print(f"修改了 {cursor.rowcount} 行")

# 查询修改后的结果
sql = """
SELECT target_col, target_header, rule_ref, rule_params_json
FROM field_pipelines
WHERE file_type = 'CUSTOMS' AND field_type = 'AI'
"""

cursor.execute(sql)
results = cursor.fetchall()

print("\n修改后的配置：")
print("+------------+--------------------------+----------------------------------------------+------------------------------------------------------+")
print("| target_col | target_header            | rule_ref                                     | rule_params_json                                     |")
print("+------------+--------------------------+----------------------------------------------+------------------------------------------------------+")
for row in results:
    print(f"| {row[0]:<10} | {row[1]:<24} | {row[2]:<44} | {row[3]:<52} |")
print("+------------+--------------------------+----------------------------------------------+------------------------------------------------------+")

conn.commit()
conn.close()
