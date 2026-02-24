"""
插入policy_copy_one_decimal的配置到rule_definitions表
"""

import pymysql
import json
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def insert_rule_definition():
    """插入policy_copy_one_decimal的配置"""
    print("=" * 100)
    print("插入policy_copy_one_decimal的配置")
    print("=" * 100)
    
    # 数据库连接配置
    db_config = {
        'host': '172.18.207.224',
        'port': 3306,
        'user': 'app',
        'password': 'app123456',
        'database': 'demo',
        'charset': 'utf8mb4'
    }
    
    try:
        # 连接数据库
        connection = pymysql.connect(**db_config)
        cursor = connection.cursor()
        
        # 插入policy_copy_one_decimal的配置
        sql = """
        INSERT INTO rule_definitions (rule_ref, rule_type, executor_type, schema_json, enabled)
        VALUES (%s, %s, %s, %s, %s)
        """
        
        rule_ref = 'policy_copy_one_decimal'
        rule_type = 'FORMAT'
        executor_type = 'program'
        schema_json = json.dumps({
            "desc": "复制源值：保留1位小数，去掉非数字和小数点的字符",
            "handler": "normalize.copy_one_decimal",
            "configurable_params": {
                "allow_null": True
            }
        }, ensure_ascii=False)
        enabled = True
        
        cursor.execute(sql, (rule_ref, rule_type, executor_type, schema_json, enabled))
        connection.commit()
        
        print(f"\n✅ policy_copy_one_decimal的配置已插入！")
        print(f"  rule_ref: {rule_ref}")
        print(f"  rule_type: {rule_type}")
        print(f"  executor_type: {executor_type}")
        print(f"  schema_json: {schema_json}")
        print(f"  enabled: {enabled}")
        
        # 关闭连接
        cursor.close()
        connection.close()
        
        print("\n" + "=" * 100)
        print("插入完成！")
        print("=" * 100)
        
    except Exception as e:
        print(f"\n❌ 插入失败: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    insert_rule_definition()
