import sqlite3
import json

def check_all_columns():
    """检查所有列的配置"""
    connection = sqlite3.connect("test.db")
    
    try:
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        
        sql = """
        SELECT target_col, target_header, map_op, source_cols, field_type, rule_ref
        FROM field_pipelines
        WHERE file_type = 'CUSTOMS' AND enabled = 1
        ORDER BY `order` ASC
        """
        cursor.execute(sql)
        results = cursor.fetchall()
        
        print("=" * 100)
        print("所有列配置")
        print("=" * 100)
        
        for row in results:
            print(f"\n列: {row['target_col']} ({row['target_header']})")
            print(f"  map_op: {row['map_op']}")
            print(f"  source_cols: {row['source_cols']}")
            print(f"  field_type: {row['field_type']}")
            print(f"  rule_ref: {row['rule_ref']}")
            print("-" * 100)
        
        print(f"\n总计: {len(results)} 个列配置")
        
    finally:
        connection.close()

if __name__ == "__main__":
    check_all_columns()
