import pymysql

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
        
        # 定义要测试的列
        test_columns = {
            'CALC': ['B', 'R'],
            'COPY': ['AG', 'AH', 'C', 'W'],
            'FORMAT': ['AA', 'L', 'M', 'U', 'Z']
        }
        
        for field_type, cols in test_columns.items():
            print(f"\n{'=' * 100}")
            print(f"测试 {field_type} 类型的列")
            print(f"{'=' * 100}")
            
            for col in cols:
                # 查询列配置
                sql = """
                SELECT target_col, target_header, map_op, field_type, rule_ref, rule_params_json
                FROM field_pipelines
                WHERE file_type = 'CUSTOMS' AND target_col = %s
                """
                
                cursor.execute(sql, (col,))
                result = cursor.fetchone()
                
                if result:
                    target_col, target_header, map_op, db_field_type, rule_ref, rule_params_json = result
                    
                    print(f"\n{target_col} ({target_header}):")
                    print(f"  map_op: {map_op}")
                    print(f"  field_type: {db_field_type}")
                    print(f"  rule_ref: {rule_ref}")
                    print(f"  rule_params_json: {rule_params_json}")
                    
                    # 根据类型给出预期结果
                    if db_field_type == 'CALC':
                        if target_col == 'B':
                            print(f"\n预期结果: 序号从1开始，每次递增1")
                        elif target_col == 'R':
                            print(f"\n预期结果: 计算发票价格，四舍五入")
                    elif db_field_type == 'COPY':
                        print(f"\n预期结果: 复制源列的值")
                    elif db_field_type == 'FORMAT':
                        print(f"\n预期结果: 格式化数据（如移除横杠、验证格式等）")
                else:
                    print(f"\n{col}: 未找到配置")
        
        connection.close()
        
        print("\n" + "=" * 100)
        print("测试完成！")
        print("=" * 100)
        
    except Exception as e:
        print(f"错误: {e}")

if __name__ == "__main__":
    test_calc_copy_format_columns()
