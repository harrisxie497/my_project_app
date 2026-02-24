"""
查询rule_ref为"policy_ai_text_dress_clean"的rule_definitions中的system_prompt
"""

import pymysql
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def query_rule_definition():
    """查询rule_ref为"policy_ai_text_dress_clean"的rule_definitions中的system_prompt"""
    print("=" * 100)
    print("查询rule_ref为\"policy_ai_text_dress_clean\"的rule_definitions中的system_prompt")
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
        
        # 查询规则定义
        sql = """
        SELECT rule_ref, rule_type, executor_type, schema_json
        FROM rule_definitions
        WHERE rule_ref = %s
        """
        
        cursor.execute(sql, ('policy_ai_text_dress_clean',))
        result = cursor.fetchone()
        
        if result:
            rule_ref, rule_type, executor_type, schema_json = result
            print(f"\nrule_ref: {rule_ref}")
            print(f"rule_type: {rule_type}")
            print(f"executor_type: {executor_type}")
            print(f"\nschema_json: {schema_json}")
            
            if schema_json and isinstance(schema_json, dict):
                system_prompt = schema_json.get('system_prompt', '')
                if system_prompt:
                    print(f"\nsystem_prompt: {system_prompt}")
        else:
            print("\n没有找到规则定义")
        
        cursor.close()
        connection.close()
        
        print("\n" + "=" * 100)
        print("查询完成！")
        print("=" * 100)
        
    except Exception as e:
        print(f"\n❌ 查询失败: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    query_rule_definition()
