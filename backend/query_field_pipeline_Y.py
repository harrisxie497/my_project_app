"""
查询Y列（收件人地址）的field_pipelines配置和AI提示词
"""

import pymysql
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def query_field_pipeline():
    """查询Y列（收件人地址）的field_pipelines配置和AI提示词"""
    print("=" * 100)
    print("查询Y列（收件人地址）的field_pipelines配置和AI提示词")
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
        
        # 查询field_pipelines
        sql = """
        SELECT target_col, target_header, map_op, field_type, rule_ref, rule_params_json
        FROM field_pipelines
        WHERE file_type = 'CUSTOMS' AND target_col = 'Y'
        """
        
        cursor.execute(sql)
        result = cursor.fetchone()
        
        if result:
            target_col, target_header, map_op, field_type, rule_ref, rule_params_json = result
            print(f"\ntarget_col: {target_col}")
            print(f"target_header: {target_header}")
            print(f"map_op: {map_op}")
            print(f"field_type: {field_type}")
            print(f"rule_ref: {rule_ref}")
            print(f"\nrule_params_json: {rule_params_json}")
            
            if rule_params_json and isinstance(rule_params_json, dict):
                prompt = rule_params_json.get(rule_ref[0], {}).get('prompt', '')
                if prompt:
                    print(f"\nfield_pipelines中的prompt: {prompt}")
        else:
            print("\n没有找到field_pipelines配置")
        
        # 查询rule_definitions中的system_prompt
        if rule_ref and isinstance(rule_ref, list) and len(rule_ref) > 0:
            sql = """
            SELECT rule_ref, schema_json
            FROM rule_definitions
            WHERE rule_ref = %s
            """
            
            cursor.execute(sql, (rule_ref[0],))
            result = cursor.fetchone()
            
            if result:
                rule_ref, schema_json = result
                print(f"\nrule_ref: {rule_ref}")
                print(f"\nschema_json: {schema_json}")
                
                if schema_json and isinstance(schema_json, dict):
                    system_prompt = schema_json.get('system_prompt', '')
                    if system_prompt:
                        print(f"\nrule_definitions中的system_prompt: {system_prompt}")
        
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
    query_field_pipeline()
