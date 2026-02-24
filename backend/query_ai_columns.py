import pymysql

def query_ai_columns():
    """查询AI类型的列"""
    print("=" * 100)
    print("查询AI类型的列")
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
        
        # 查询AI类型的列
        sql = """
        SELECT target_col, target_header, map_op, field_type, rule_ref, rule_params_json, depends_on
        FROM field_pipelines
        WHERE file_type = 'CUSTOMS' AND field_type = 'AI'
        ORDER BY target_col
        """
        
        cursor.execute(sql)
        results = cursor.fetchall()
        
        print(f"\n找到 {len(results)} 个AI类型的列:\n")
        
        for result in results:
            target_col, target_header, map_op, field_type, rule_ref, rule_params_json, depends_on = result
            
            print(f"{target_col} ({target_header}):")
            print(f"  map_op: {map_op}")
            print(f"  field_type: {field_type}")
            print(f"  rule_ref: {rule_ref}")
            print(f"  depends_on: {depends_on}")
            print(f"  rule_params_json: {rule_params_json}")
            print()
        
        connection.close()
        
        print("=" * 100)
        print("查询完成！")
        print("=" * 100)
        
    except Exception as e:
        print(f"错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    query_ai_columns()
