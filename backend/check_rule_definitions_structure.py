import pymysql

conn = pymysql.connect(
    host='172.18.207.224',
    user='app',
    password='app123456',
    database='demo',
    charset='utf8mb4'
)

cursor = conn.cursor(pymysql.cursors.DictCursor)

# 查询rule_definitions表的结构
cursor.execute('DESCRIBE rule_definitions')
results = cursor.fetchall()

for row in results:
    print(f'{row["Field"]}: {row["Type"]}')

conn.close()
