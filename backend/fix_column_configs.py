import sqlite3

def fix_column_configs():
    """修复列配置"""
    connection = sqlite3.connect("test.db")
    
    try:
        cursor = connection.cursor()
        
        # 修复B列：将map_op从COPY改为CALC
        print("修复B列配置...")
        cursor.execute("""
            UPDATE field_pipelines
            SET map_op = 'CALC'
            WHERE file_type = 'CUSTOMS' AND target_col = 'B'
        """)
        print(f"  影响行数: {cursor.rowcount}")
        
        # 修复AG列：将map_op从COPY改为CALC
        print("\n修复AG列配置...")
        cursor.execute("""
            UPDATE field_pipelines
            SET map_op = 'CALC'
            WHERE file_type = 'CUSTOMS' AND target_col = 'AG'
        """)
        print(f"  影响行数: {cursor.rowcount}")
        
        # 修复AH列：将map_op从COPY改为CALC
        print("\n修复AH列配置...")
        cursor.execute("""
            UPDATE field_pipelines
            SET map_op = 'CALC'
            WHERE file_type = 'CUSTOMS' AND target_col = 'AH'
        """)
        print(f"  影响行数: {cursor.rowcount}")
        
        connection.commit()
        print("\n配置修复完成！")
        
    except Exception as e:
        print(f"修复失败: {e}")
        connection.rollback()
    finally:
        connection.close()

if __name__ == "__main__":
    fix_column_configs()
