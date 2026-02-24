"""
查询非AI列的field_pipelines配置
"""

import pymysql
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def query_field_pipelines():
    """查询非AI列的field_pipelines配置"""
    print("=" * 100)
    print("查询非AI列的field_pipelines配置")
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
        
        # 查询非AI列的field_pipelines
        target_cols = ['A', 'E', 'G', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'V', 'W', 'X', 'Y', 'Z', 'AA', 'AB', 'AC', 'AD', 'AE', 'AF', 'AG', 'AH', 'AI', 'AJ', 'AK', 'AL', 'AM', 'AN', 'AO']
        
        for target_col in target_cols:
            sql = """
            SELECT target_col, target_header, map_op, field_type, rule_ref, rule_params_json
            FROM field_pipelines
            WHERE file_type = 'CUSTOMS' AND target_col = %s
            """
            
            cursor.execute(sql, (target_col,))
            result = cursor.fetchone()
            
            if result:
                target_col, target_header, map_op, field_type, rule_ref, rule_params_json = result
                print(f"\n{target_col} ({target_header}):")
                print(f"  map_op: {map_op}")
                print(f"  field_type: {field_type}")
                print(f"  rule_ref: {rule_ref}")
                print(f"  rule_params_json: {rule_params_json}")
        
        cursor.close()
        connection.close()
        
        print("\n" + "=" * 100)
        print("查询完成！")
        print("=" * 100)
        
    except Exception as e:
        print(f"\n❌ 查询失败: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    query_field_pipelines()
