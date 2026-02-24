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

# 查询H列和Y列的配置
cursor.execute('''
    SELECT 
        fp.id,
        fp.target_col,
        fp.target_header,
        fp.file_type,
        fp.map_op,
        fp.field_type,
        fp.source_cols,
        fp.depends_on,
        fp.rule_ref,
        fp.rule_params_json,
        fp.enabled,
        rd.schema_json
    FROM field_pipelines fp
    LEFT JOIN rule_definitions rd ON fp.rule_ref LIKE CONCAT('%', rd.rule_ref, '%')
    WHERE fp.target_col IN ('H', 'Y') AND fp.file_type = 'CUSTOMS'
    ORDER BY fp.target_col, fp.id
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
    print(f'schema_json: {row["schema_json"]}')
    print()

conn.close()
