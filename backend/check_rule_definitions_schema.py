import pymysql

def check_rule_definitions_schema():
    """检查rule_definitions表中的schema_json字段"""
    print("=" * 100)
    print("检查rule_definitions表中的schema_json字段")
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
        
        # 查询AI规则的schema_json
        sql = """
        SELECT rule_ref, schema_json
        FROM rule_definitions
        WHERE rule_ref IN ('policy_ai_text_ja_clean', 'policy_ai_text_dress_clean', 'policy_translate_from_targetcol_en_upper')
        """
        
        cursor.execute(sql)
        results = cursor.fetchall()
        
        print(f"\n找到 {len(results)} 个AI规则:\n")
        
        for result in results:
            rule_ref, schema_json = result
            
            print(f"{rule_ref}:")
            print(f"  schema_json类型: {type(schema_json)}")
            print(f"  schema_json长度: {len(schema_json) if isinstance(schema_json, str) else 'N/A'}")
            print(f"  schema_json前200个字符: {str(schema_json)[:200]}")
            print()
        
        connection.close()
        
        print("=" * 100)
        print("检查完成！")
        print("=" * 100)
        
    except Exception as e:
        print(f"错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    check_rule_definitions_schema()
