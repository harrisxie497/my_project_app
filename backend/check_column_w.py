import sqlite3
import json

def check_column_w():
    """检查W列的配置"""
    connection = sqlite3.connect("test.db")
    
    try:
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        
        sql = """
        SELECT target_col, target_header, map_op, source_cols, field_type, rule_ref
        FROM field_pipelines
        WHERE file_type = 'CUSTOMS' AND target_col = 'W' AND enabled = 1
        """
        cursor.execute(sql)
        result = cursor.fetchone()
        
        if result:
            print("=" * 100)
            print("W列配置")
            print("=" * 100)
            print(f"目标列: {result['target_col']}")
            print(f"目标表头: {result['target_header']}")
            print(f"map_op: {result['map_op']}")
            print(f"source_cols: {result['source_cols']}")
            print(f"field_type: {result['field_type']}")
            print(f"rule_ref: {result['rule_ref']}")
        else:
            print("W列配置不存在")
        
    finally:
        connection.close()

if __name__ == "__main__":
    check_column_w()
