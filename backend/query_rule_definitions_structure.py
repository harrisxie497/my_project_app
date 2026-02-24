"""
查询rule_definitions表的结构
"""

import pymysql
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def query_rule_definitions_structure():
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
        
        print(f"\n找到 {len(results)} 条记录")
        
        for row in results:
            field, type, null, key, default, extra = row
            
            print(f"\n{'=' * 100}")
            print(f"field: {field}")
            print(f"type: {type}")
            print(f"null: {null}")
            print(f"key: {key}")
            print(f"default: {default}")
            print(f"extra: {extra}")
        
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
    query_rule_definitions_structure()
