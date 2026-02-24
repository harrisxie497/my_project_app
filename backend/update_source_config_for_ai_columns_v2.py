import pymysql
import json

def update_source_config_for_ai_columns_v2():
    """更新SOURCE配置中AI列的定义（版本2）"""
    print("=" * 100)
    print("更新SOURCE配置中AI列的定义（版本2）")
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
        
        # 查询SOURCE配置
        sql = """
        SELECT id, columns_json
        FROM file_definitions
        WHERE file_type = 'CUSTOMS' AND file_role = 'SOURCE'
        """
        
        cursor.execute(sql)
        result = cursor.fetchone()
        
        if result:
            config_id = result[0]
            columns_json_str = result[1]
            
            # 解析JSON
            columns_json = json.loads(columns_json_str) if isinstance(columns_json_str, str) else columns_json_str
            
            print(f"\n原始SOURCE配置:")
            print(f"  配置ID: {config_id}")
            print(f"  列数: {len(columns_json)}")
            
            # 更新AI列的定义
            ai_columns_mapping = {
                'AD': '收件人名（日文）',  # X列应该对应AD列
                'M': '收件人地址',         # Y列应该对应M列
                'K': '輸入者名',          # J列应该对应K列
                'N': '輸入者住所'          # K列应该对应N列
            }
            
            updated_count = 0
            for col_def in columns_json:
                col_letter = col_def.get('col')
                col_header = col_def.get('header')
                
                if col_letter in ai_columns_mapping:
                    new_header = ai_columns_mapping[col_letter]
                    if col_header != new_header:
                        print(f"\n更新列: {col_letter}")
                        print(f"  旧表头: {col_header}")
                        print(f"  新表头: {new_header}")
                        col_def['header'] = new_header
                        updated_count += 1
            
            if updated_count > 0:
                # 更新数据库
                updated_json = json.dumps(columns_json, ensure_ascii=False)
                update_sql = """
                UPDATE file_definitions
                SET columns_json = %s, updated_at = NOW()
                WHERE id = %s
                """
                cursor.execute(update_sql, (updated_json, config_id))
                connection.commit()
                
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
    update_source_config_for_ai_columns_v2()
