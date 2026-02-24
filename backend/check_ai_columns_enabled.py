import pymysql

def check_ai_columns_enabled():
    """检查AI列的enabled字段和depends_on字段"""
    print("=" * 100)
    print("检查AI列的enabled字段和depends_on字段")
    print("=" * 100)
    
    try:
        connection = pymysql.connect(
            host='172.18.207.224',
            port=3306,
            user='app',
            password='app123456',
            database='demo',
            charset='utf8mb4'
        )
        cursor = connection.cursor()
        
        # 查询AI列的配置
        sql = """
        SELECT target_col, target_header, map_op, source_cols, field_type, rule_ref, depends_on, enabled
        FROM field_pipelines
        WHERE file_type = 'CUSTOMS' AND field_type = 'AI'
        ORDER BY target_col
        """
        
        cursor.execute(sql)
        results = cursor.fetchall()
        
        print(f"\n找到 {len(results)} 个AI列的配置:\n")
        
        for result in results:
            target_col, target_header, map_op, source_cols, field_type, rule_ref, depends_on, enabled = result
            
            print(f"{target_col} ({target_header}):")
            print(f"  map_op: {map_op}")
            print(f"  source_cols: {source_cols}")
            print(f"  field_type: {field_type}")
            print(f"  rule_ref: {rule_ref}")
            print(f"  depends_on: {depends_on}")
            print(f"  enabled: {enabled}")
            print()
        
        connection.close()
        
        print("=" * 100)
        print("检查完成！")
        print("=" * 100)
        
    except Exception as e:
        print(f"错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    check_ai_columns_enabled()
