"""
测试CALC、COPY、FORMAT类型的列（直接运行SQL查询）
"""

import pymysql
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def test_simple_columns():
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
        
        # 直接运行SQL查询，看看是否能够查询到数据
        sql = """
        SELECT target_col, target_header, map_op, field_type, rule_ref, rule_params_json
        FROM field_pipelines
        WHERE file_type = 'CUSTOMS' AND target_col IN ('R', 'W', 'Z', 'AA')
        """
        
        print(f"执行SQL查询: {sql}")
        cursor.execute(sql)
        results = cursor.fetchall()
        
        print(f"查询结果数量: {len(results)}")
        
        for result in results:
            target_col, target_header, map_op, field_type, rule_ref, rule_params_json = result
            print(f"\n{target_col} ({target_header}):")
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
    test_simple_columns()
