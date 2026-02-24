"""
检查policy_translate_from_targetcol_en_upper规则的配置
"""

import pymysql
import json

def check_translate_rule_config():
    """检查policy_translate_from_targetcol_en_upper规则的配置"""
    print("=" * 100)
    print("检查policy_translate_from_targetcol_en_upper规则的配置")
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
        
        # 查询规则配置
        sql = """
        SELECT rule_ref, rule_type, executor_type, schema_json, enabled
        FROM rule_definitions
        WHERE rule_ref = 'policy_translate_from_targetcol_en_upper'
        """
        
        cursor.execute(sql)
        results = cursor.fetchall()
        
        print(f"\n找到 {len(results)} 个规则配置:\n")
        
        for result in results:
            rule_ref, rule_type, executor_type, schema_json, enabled = result
            
            print(f"规则引用: {rule_ref}")
            print(f"规则类型: {rule_type}")
            print(f"执行器类型: {executor_type}")
            print(f"启用: {enabled}")
            
            # 解析schema_json
            if schema_json:
                schema = json.loads(schema_json)
                print(f"\nSchema JSON:")
                print(json.dumps(schema, indent=2, ensure_ascii=False))
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
    check_translate_rule_config()
