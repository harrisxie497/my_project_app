"""
测试const类型的列
"""

import pymysql
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def test_const_columns():
    """测试const类型的列"""
    print("=" * 100)
    print("测试const类型的列")
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
        
        # 查询const类型的列
        target_cols = ['A', 'E', 'G', 'N', 'O', 'P', 'Q', 'S', 'T', 'V', 'AE', 'AF', 'AI']
        
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
                
                # 预期结果
                if isinstance(rule_params_json, str):
                    import json
                    rule_params_json = json.loads(rule_params_json)
                
                if 'policy_const' in rule_params_json:
                    const_value = rule_params_json['policy_const'].get('value', '')
                    print(f"\n预期结果: {const_value}")
                else:
                    print(f"\n预期结果: 无法确定")
        
        cursor.close()
        connection.close()
        
        print("\n" + "=" * 100)
        print("测试完成！")
        print("=" * 100)
        
    except Exception as e:
        print(f"\n❌ 测试失败: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    test_const_columns()
