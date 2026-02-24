import pymysql

def update_field_pipelines_for_ai_columns():
    """更新field_pipelines中AI列的source_cols配置"""
    print("=" * 100)
    print("更新field_pipelines中AI列的source_cols配置")
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
        
        # 定义AI列的source_cols映射
        ai_columns_mapping = {
            'X': ['AD'],  # 收件人名（日文）从AD列读取
            'Y': ['M'],   # 收件人地址从M列读取
            'J': ['K'],   # 輸入者名从K列读取
            'K': ['N']    # 輸入者住所从N列读取
        }
        
        updated_count = 0
        for target_col, new_source_cols in ai_columns_mapping.items():
            # 查询当前配置
            sql = """
            SELECT target_col, target_header, source_cols
            FROM field_pipelines
            WHERE file_type = 'CUSTOMS' AND target_col = %s
            """
            
            cursor.execute(sql, (target_col,))
            result = cursor.fetchone()
            
            if result:
                current_target_col, target_header, current_source_cols = result
                
                # 将source_cols转换为字符串进行比较
                current_source_cols_str = str(current_source_cols) if current_source_cols else '[]'
                new_source_cols_str = str(new_source_cols)
                
                if current_source_cols_str != new_source_cols_str:
                    print(f"\n更新列: {target_col} ({target_header})")
                    print(f"  旧source_cols: {current_source_cols}")
                    print(f"  新source_cols: {new_source_cols}")
                    
                    # 更新配置
                    import json
                    update_sql = """
                    UPDATE field_pipelines
                    SET source_cols = %s, updated_at = NOW()
                    WHERE file_type = 'CUSTOMS' AND target_col = %s
                    """
                    cursor.execute(update_sql, (json.dumps(new_source_cols), target_col))
                    connection.commit()
                    
                    updated_count += 1
                else:
                    print(f"\n{target_col} ({target_header}): source_cols已经是正确的")
        
        if updated_count > 0:
            print(f"\n✅ 更新完成！共更新了{updated_count}列")
        else:
            print(f"\n❌ 没有需要更新的列")
        
        connection.close()
        
        print("\n" + "=" * 100)
        print("更新完成！")
        print("=" * 100)
        
    except Exception as e:
        print(f"错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    update_field_pipelines_for_ai_columns()
