"""
检查記事欄2列的FieldPipeline配置
"""
import pymysql

# MySQL配置
MYSQL_CONFIG = {
    'host': '172.18.207.224',
    'port': 3306,
    'user': 'root',
    'password': 'root123456',
    'database': 'demo'
}

print("=" * 80)
print("查询記事欄2列的FieldPipeline配置")
print("=" * 80)

try:
    connection = pymysql.connect(**MYSQL_CONFIG)
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    
    # 查询DELIVERY的OUTPUT中"記事欄2"（P列）的FieldPipeline
    cursor.execute("""
        SELECT id, file_type, file_role, target_col, source_cols,
               map_op, rule_ref, rule_params_json
        FROM field_pipelines
        WHERE file_type = 'DELIVERY'
          AND file_role = 'OUTPUT'
          AND target_col = 'P'
    """)
    
    result = cursor.fetchone()
    
    if result:
        print("\n【記事欄2（P列）配置】")
        print(f"ID: {result['id']}")
        print(f"目标列: {result['target_col']}")
        print(f"源列: {result['source_cols']}")
        print(f"操作: {result['map_op']}")
        print(f"规则引用: {result['rule_ref']}")
        print(f"规则参数: {result['rule_params_json']}")
    else:
        print("\n[FAIL] 未找到記事欄2（P列）的配置")
    
    # 查询所有DELIVERY的OUTPUT配置
    print("\n" + "=" * 80)
    print("【所有DELIVERY OUTPUT配置】")
    print("=" * 80)
    cursor.execute("""
        SELECT target_col, source_cols, map_op, rule_ref, rule_params_json
        FROM field_pipelines
        WHERE file_type = 'DELIVERY' AND file_role = 'OUTPUT'
        ORDER BY target_col
    """)
    
    results = cursor.fetchall()
    
    if results:
        print(f"\n共有 {len(results)} 个列配置：\n")
        for i, row in enumerate(results, 1):
            print(f"{i}. {row['target_col']}: {row['map_op']} | source_cols={row['source_cols']} | rule_ref={row['rule_ref']}")
    
    cursor.close()
    connection.close()
    
    print("\n" + "=" * 80)
    
except Exception as e:
    print(f"\n[FAIL] 错误: {str(e)}")
    import traceback
    traceback.print_exc()
