import pymysql

def query_all_map_ops():
    """查询所有不同的map_op类型"""
    print("=" * 100)
    print("查询所有不同的map_op类型")
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
        
        # 查询所有不同的map_op类型
        sql = """
        SELECT DISTINCT map_op, field_type
        FROM field_pipelines
        WHERE file_type = 'CUSTOMS'
        ORDER BY map_op, field_type
        """
        
        cursor.execute(sql)
        results = cursor.fetchall()
        
        print(f"\n找到 {len(results)} 种不同的map_op和field_type组合:\n")
        
        for result in results:
            map_op, field_type = result
            print(f"  map_op: {map_op}, field_type: {field_type}")
        
        # 查询map_op = 'CALC'的列
        print("\n" + "=" * 100)
        print("查询map_op = 'CALC'的列")
        print("=" * 100)
        
        sql = """
        SELECT target_col, target_header, map_op, field_type, rule_ref, rule_params_json
        FROM field_pipelines
        WHERE file_type = 'CUSTOMS' AND map_op = 'CALC'
        ORDER BY target_col
        """
        
        cursor.execute(sql)
        results = cursor.fetchall()
        
        print(f"\n找到 {len(results)} 个map_op = 'CALC'的列:\n")
        
        for result in results:
            target_col, target_header, map_op, field_type, rule_ref, rule_params_json = result
            
            print(f"{target_col} ({target_header}):")
            print(f"  map_op: {map_op}")
            print(f"  field_type: {field_type}")
            print(f"  rule_ref: {rule_ref}")
            print(f"  rule_params_json: {rule_params_json}")
            print()
        
        connection.close()
        
        print("=" * 100)
        print("查询完成！")
        print("=" * 100)
        
    except Exception as e:
        print(f"错误: {e}")

if __name__ == "__main__":
    query_all_map_ops()
