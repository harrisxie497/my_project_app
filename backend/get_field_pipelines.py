import sqlite3
import json

def get_field_pipelines():
    """获取field_pipelines配置"""
    connection = sqlite3.connect("test.db")
    
    try:
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        
        sql = """
        SELECT target_col, target_header, map_op, source_cols, field_type, rule_ref, depends_on, `order`, enabled
        FROM field_pipelines
        WHERE file_type = 'CUSTOMS' AND enabled = 1
        ORDER BY `order` ASC
        """
        cursor.execute(sql)
        results = cursor.fetchall()
        
        print("=" * 100)
        print("FIELD_PIPELINES 配置列表")
        print("=" * 100)
        
        for row in results:
            target_col = row['target_col']
            target_header = row['target_header']
            map_op = row['map_op']
            source_cols = json.loads(row['source_cols']) if row['source_cols'] else []
            field_type = row['field_type']
            rule_ref = json.loads(row['rule_ref']) if row['rule_ref'] else []
            depends_on = json.loads(row['depends_on']) if row['depends_on'] else []
            order = row['order']
            enabled = row['enabled']
            
            print(f"\n列: {target_col} ({target_header})")
            print(f"  map_op: {map_op}")
            print(f"  source_cols: {source_cols}")
            print(f"  field_type: {field_type}")
            print(f"  rule_ref: {rule_ref}")
            print(f"  depends_on: {depends_on}")
            print(f"  order: {order}")
            print(f"  enabled: {enabled}")
            
            # 分析处理函数
            print(f"\n  处理函数分析:")
            if map_op == 'COPY':
                print(f"    函数: copy_field()")
                if source_cols and len(source_cols) > 0:
                    print(f"    输入: row['{source_cols[0]}'] (源列的值)")
                else:
                    print(f"    输入: 无 (source_cols为空)")
                print(f"    输出: 复制后的值")
            elif map_op == 'CONST':
                print(f"    函数: set_constant('')")
                print(f"    输入: 无")
                print(f"    输出: 空字符串")
            elif map_op == 'NONE':
                print(f"    函数: None")
                print(f"    输入: 无")
                print(f"    输出: None")
            elif map_op == 'CALC':
                if 'seq_from_1' in rule_ref:
                    print(f"    函数: generate_sequence(row['_row_index'])")
                    print(f"    输入: row['_row_index'] (行索引)")
                    print(f"    输出: 序列号 (从1开始)")
                elif 'copy_equal_to' in rule_ref:
                    print(f"    函数: copy_equal_to(row['D'], row['C'])")
                    print(f"    输入: row['D'] (源值), row['C'] (目标值)")
                    print(f"    输出: 如果源值不为空则返回源值，否则返回目标值")
                elif 'calc_invoice_price_fx_round' in rule_ref:
                    print(f"    函数: calc_invoice_price_fx_round(row['R'], row['Q'], exchange_rate_service)")
                    print(f"    输入: row['R'] (原价), row['Q'] (货币代码), exchange_rate_service (汇率服务)")
                    print(f"    输出: 汇率转换后的价格（四舍五入）")
                else:
                    print(f"    函数: 未知")
                    print(f"    输入: 未知")
                    print(f"    输出: 未知")
            
            print("-" * 100)
        
        print(f"\n总计: {len(results)} 个字段配置")
        
    finally:
        connection.close()

if __name__ == "__main__":
    get_field_pipelines()
