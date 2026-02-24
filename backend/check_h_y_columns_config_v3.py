import pymysql
import json
import sys

# 设置输出编码为UTF-8
sys.stdout.reconfigure(encoding='utf-8')

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

# 将结果保存到文件
with open('h_y_columns_config.txt', 'w', encoding='utf-8') as f:
    for row in results:
        f.write('=' * 100 + '\n')
        f.write(f'ID: {row["id"]}\n')
        f.write(f'列: {row["target_col"]} - {row["target_header"]}\n')
        f.write(f'file_type: {row["file_type"]}\n')
        f.write(f'map_op: {row["map_op"]}\n')
        f.write(f'field_type: {row["field_type"]}\n')
        f.write(f'source_cols: {row["source_cols"]}\n')
        f.write(f'depends_on: {row["depends_on"]}\n')
        f.write(f'rule_ref: {row["rule_ref"]}\n')
        f.write(f'rule_params_json: {row["rule_params_json"]}\n')
        f.write(f'enabled: {row["enabled"]}\n')
        f.write(f'schema_json: {row["schema_json"]}\n')
        f.write('\n')

print('配置已保存到 h_y_columns_config.txt 文件中')

conn.close()
