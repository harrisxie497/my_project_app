"""
查询rule_definitions表的结构
"""

import pymysql
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def query_rule_definitions():
    """查询rule_definitions表的结构"""
    print("=" * 100)
    print("查询rule_definitions表的结构")
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
        
        # 查询rule_definitions表的结构
        sql = """
        SHOW COLUMNS FROM rule_definitions
        """
        
        cursor.execute(sql)
        results = cursor.fetchall()
        
        print(f"\nrule_definitions表的字段:")
        for row in results:
            print(f"  {row}")
        
        # 查询rule_definitions表的数据
        sql = """
        SELECT rule_ref, schema_json
        FROM rule_definitions
        WHERE rule_ref IN ('policy_ai_goods_en', 'policy_ai_material_en', 'policy_ai_text_ja_clean', 'policy_ai_text_dress_clean', 'policy_translate_from_targetcol_en_upper')
        """
        
        cursor.execute(sql)
        results = cursor.fetchall()
        
        print(f"\nrule_definitions表的数据:")
        for row in results:
            rule_ref, schema_json = row
            print(f"\n  rule_ref: {rule_ref}")
            print(f"  schema_json: {schema_json}")
        
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
    query_rule_definitions()
