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
    
    # 先查看表结构
    print("\n【field_pipelines表结构】")
    cursor.execute("DESCRIBE field_pipelines")
    columns = cursor.fetchall()
    for col in columns:
        print(f"  {col['Field']}: {col['Type']}")
    
    # 查询DELIVERY的OUTPUT中"記事欄2"（P列）的FieldPipeline
    print("\n" + "=" * 80)
    print("\n【記事欄2（P列）配置】")
    cursor.execute("""
        SELECT *
        FROM field_pipelines
        WHERE file_type = 'DELIVERY'
          AND target_col = 'P'
    """)
    
    result = cursor.fetchone()
    
    if result:
        for key, value in result.items():
            print(f"  {key}: {value}")
    else:
        print("  [FAIL] 未找到記事欄2（P列）的配置")
    
    # 查询所有DELIVERY的OUTPUT配置
    print("\n" + "=" * 80)
    print("\n【所有DELIVERY配置】")
    cursor.execute("""
        SELECT target_col, source_cols, map_op, rule_ref, rule_params_json
        FROM field_pipelines
        WHERE file_type = 'DELIVERY'
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
