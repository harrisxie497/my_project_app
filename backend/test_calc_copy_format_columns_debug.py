"""
测试CALC、COPY、FORMAT类型的列（添加更多调试信息）
"""

import pymysql
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def test_calc_copy_format_columns():
    """测试CALC、COPY、FORMAT类型的列"""
    print("=" * 100)
    print("测试CALC、COPY、FORMAT类型的列")
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
        
        # 查询CALC、COPY、FORMAT类型的列
        target_cols = {
            'CALC': 'R (インボイス価格)',
            'COPY': 'W (備考)',
            'FORMAT': 'Z (收件人电话)',
            'FORMAT': 'AA (收件人邮编)'
        }
        
        print(f"查询的列: {list(target_cols.keys())}")
        
        for target_col, description in target_cols.items():
            sql = """
            SELECT target_col, target_header, map_op, field_type, rule_ref, rule_params_json
            FROM field_pipelines
            WHERE file_type = 'CUSTOMS' AND target_col = %s
            """
            
            print(f"执行SQL查询: {sql}")
            print(f"SQL参数: {target_col}")
            
            cursor.execute(sql, (target_col,))
            result = cursor.fetchone()
            
            print(f"查询结果: {result}")
            
            if result:
                target_col, target_header, map_op, field_type, rule_ref, rule_params_json = result
                print(f"\n{target_col} ({description}):")
                print(f"  map_op: {map_op}")
                print(f"  field_type: {field_type}")
                print(f"  rule_ref: {rule_ref}")
                print(f"  rule_params_json: {rule_params_json}")
                
                # 预期结果
                if map_op == 'CALC':
                    print(f"\n预期结果: 需要计算并四舍五入")
                elif map_op == 'COPY':
                    print(f"\n预期结果: 复制源列的值")
                elif map_op == 'FORMAT':
                    print(f"\n预期结果: 需要格式化")
                else:
                    print(f"\n预期结果: 无法确定")
            else:
                print(f"\n{target_col} ({description}): 未找到配置")
        
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
    test_calc_copy_format_columns()
