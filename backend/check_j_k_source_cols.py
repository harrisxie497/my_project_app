import pymysql

connection = pymysql.connect(
    host='172.18.207.224',
    port=3306,
    user='app',
    password='app123456',
    database='demo',
    charset='utf8mb4'
)

cursor = connection.cursor()

sql = "SELECT target_col, source_cols FROM field_pipelines WHERE file_type = 'CUSTOMS' AND target_col IN ('J', 'K')"
cursor.execute(sql)
results = cursor.fetchall()

print('=== J列和K列的source_cols配置 ===')
for row in results:
    print(f'target_col: {row[0]}, source_cols: {row[1]}')

cursor.close()
connection.close()
