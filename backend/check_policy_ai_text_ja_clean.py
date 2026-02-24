"""
检查policy_ai_text_ja_clean规则是否正确实现了
"""

import pymysql
import json
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def check_policy_ai_text_ja_clean():
    """检查policy_ai_text_ja_clean规则是否正确实现了"""
    print("=" * 100)
    print("检查policy_ai_text_ja_clean规则是否正确实现了")
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
        
        # 查询policy_ai_text_ja_clean的配置
        sql = """
        SELECT rule_ref, rule_type, executor_type, schema_json, enabled
        FROM rule_definitions
        WHERE rule_ref = 'policy_ai_text_ja_clean'
        """
        
        cursor.execute(sql)
        results = cursor.fetchall()
        
        print(f"\n找到 {len(results)} 条记录")
        
        if results:
            for row in results:
                rule_ref, rule_type, executor_type, schema_json, enabled = row
                
                print(f"\n{'=' * 100}")
                print(f"rule_ref: {rule_ref}")
                print(f"rule_type: {rule_type}")
                print(f"executor_type: {executor_type}")
                print(f"schema_json: {schema_json}")
                print(f"enabled: {enabled}")
        else:
            print(f"\n⚠️ 没有找到policy_ai_text_ja_clean的配置")
        
        # 关闭连接
        cursor.close()
        connection.close()
        
        print("\n" + "=" * 100)
        print("检查完成！")
        print("=" * 100)
        
    except Exception as e:
        print(f"\n❌ 检查失败: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    check_policy_ai_text_ja_clean()
