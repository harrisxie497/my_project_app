import pymysql

def check_copy_columns_config():
    """检查COPY类型列的配置"""
    print("=" * 100)
    print("检查COPY类型列的配置")
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
        
        # 检查COPY类型列的配置
        check_columns = ['HAWB番号', '現地問合せ番号', '貨物重量', '輸入者 郵便番号', '輸入者電話番号']
        
        for header in check_columns:
            sql = """
            SELECT target_col, target_header, map_op, field_type, rule_ref, rule_params_json, source_cols
            FROM field_pipelines
            WHERE file_type = 'CUSTOMS' AND target_header = %s
            """
            
            cursor.execute(sql, (header,))
            result = cursor.fetchone()
            
            if result:
                target_col, target_header, map_op, field_type, rule_ref, rule_params_json, source_cols = result
                
                print(f"\n{target_header}:")
                print(f"  target_col: {target_col}")
                print(f"  map_op: {map_op}")
                print(f"  field_type: {field_type}")
                print(f"  rule_ref: {rule_ref}")
                print(f"  rule_params_json: {rule_params_json}")
                print(f"  source_cols: {source_cols}")
            else:
                print(f"\n{header}: 未找到配置")
        
        connection.close()
        
        print("\n" + "=" * 100)
        print("检查完成！")
        print("=" * 100)
        
    except Exception as e:
        print(f"错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    check_copy_columns_config()
