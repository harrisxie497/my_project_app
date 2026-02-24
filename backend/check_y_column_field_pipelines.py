"""
检查Y列的field_pipelines配置
"""

import pymysql

def check_y_column_field_pipelines():
    """检查Y列的field_pipelines配置"""
    print("=" * 100)
    print("检查Y列的field_pipelines配置")
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
        
        # 查询Y列的配置
        sql = """
        SELECT target_col, target_header, map_op, source_cols, field_type, rule_ref, depends_on, enabled
        FROM field_pipelines
        WHERE file_type = 'CUSTOMS' AND target_col = 'Y'
        """
        
        cursor.execute(sql)
        results = cursor.fetchall()
        
        print(f"\n找到 {len(results)} 个Y列的配置:\n")
        
        for result in results:
            target_col, target_header, map_op, source_cols, field_type, rule_ref, depends_on, enabled = result
            
            print(f"目标列: {target_col}")
            print(f"目标表头: {target_header}")
            print(f"操作类型: {map_op}")
            print(f"源列: {source_cols}")
            print(f"字段类型: {field_type}")
            print(f"规则引用: {rule_ref}")
            print(f"依赖列: {depends_on}")
            print(f"启用: {enabled}")
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
    check_y_column_field_pipelines()
