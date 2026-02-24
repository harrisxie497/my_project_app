"""
查询AI规则policy_translate_from_targetcol_en_upper的配置
"""

import pymysql
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def query_ai_rule_config_translate():
    """查询AI规则policy_translate_from_targetcol_en_upper的配置"""
    print("=" * 100)
    print("查询AI规则policy_translate_from_targetcol_en_upper的配置")
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
        
        # 查询AI规则policy_translate_from_targetcol_en_upper的配置
        sql = """
        SELECT rule_ref, schema_json
        FROM rule_definitions
        WHERE rule_ref = 'policy_translate_from_targetcol_en_upper'
        """
        
        cursor.execute(sql)
        results = cursor.fetchall()
        
        print(f"\n找到 {len(results)} 条记录")
        
        for row in results:
            rule_ref, schema_json = row
            
            print(f"\n{'=' * 100}")
            print(f"rule_ref: {rule_ref}")
            print(f"schema_json: {schema_json}")
        
        # 关闭连接
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
    query_ai_rule_config_translate()
