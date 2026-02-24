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

# 查询J列和K列的配置
cursor.execute('''
    SELECT 
        fp.target_col,
        fp.target_header,
        fp.map_op,
        fp.field_type,
        fp.source_cols,
        fp.depends_on,
        fp.rule_ref,
        fp.rule_params_json,
        rd.schema_json
    FROM field_pipelines fp
    LEFT JOIN rule_definitions rd ON fp.rule_ref LIKE CONCAT('%', rd.rule_ref, '%')
    WHERE fp.target_col IN ('J', 'K')
    ORDER BY fp.target_col
''')

results = cursor.fetchall()

for row in results:
    print('=' * 100)
    print(f'列: {row["target_col"]} - {row["target_header"]}')
    print('=' * 100)
    print(f'map_op: {row["map_op"]}')
    print(f'field_type: {row["field_type"]}')
    print(f'source_cols: {row["source_cols"]}')
    print(f'depends_on: {row["depends_on"]}')
    print(f'rule_ref: {row["rule_ref"]}')
    print(f'rule_params_json: {row["rule_params_json"]}')
    print(f'schema_json: {row["schema_json"]}')
    print()

conn.close()
