"""
查询数据库中是否有存储提示词的字段
"""

import pymysql
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def query_prompt_fields():
    """查询数据库中是否有存储提示词的字段"""
    print("=" * 100)
    print("查询数据库中是否有存储提示词的字段")
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
        
        # 查询field_pipelines表的结构
        sql = """
        SHOW COLUMNS FROM field_pipelines
        """
        
        cursor.execute(sql)
        results = cursor.fetchall()
        
        print(f"\nfield_pipelines表的字段:")
        for row in results:
            print(f"  {row}")
        
        # 查询AI规则的rule_params_json
        sql = """
        SELECT target_col, target_header, rule_ref, rule_params_json
        FROM field_pipelines
        WHERE file_type = 'CUSTOMS' AND field_type = 'AI'
        """
        
        cursor.execute(sql)
        results = cursor.fetchall()
        
        print(f"\nAI规则的rule_params_json:")
        for row in results:
            target_col, target_header, rule_ref, rule_params_json = row
            print(f"\n  target_col: {target_col}")
            print(f"  target_header: {target_header}")
            print(f"  rule_ref: {rule_ref}")
            print(f"  rule_params_json: {rule_params_json}")
        
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
    query_prompt_fields()
