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

# 查询所有J列和K列的配置
cursor.execute('''
    SELECT 
        id,
        file_type,
        target_col,
        target_header,
        map_op,
        field_type,
        source_cols,
        depends_on,
        rule_ref,
        rule_params_json,
        enabled
    FROM field_pipelines
    WHERE target_col IN ('J', 'K')
    ORDER BY target_col, id
''')

results = cursor.fetchall()

for row in results:
    print('=' * 100)
    print(f'ID: {row["id"]}')
    print(f'列: {row["target_col"]} - {row["target_header"]}')
    print(f'file_type: {row["file_type"]}')
    print(f'map_op: {row["map_op"]}')
    print(f'field_type: {row["field_type"]}')
    print(f'source_cols: {row["source_cols"]}')
    print(f'depends_on: {row["depends_on"]}')
    print(f'rule_ref: {row["rule_ref"]}')
    print(f'rule_params_json: {row["rule_params_json"]}')
    print(f'enabled: {row["enabled"]}')
    print()

conn.close()
