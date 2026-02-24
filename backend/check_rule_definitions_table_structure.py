"""
查看rule_definitions表的结构
"""

import pymysql

def check_rule_definitions_table_structure():
    """查看rule_definitions表的结构"""
    print("=" * 100)
    print("查看rule_definitions表的结构")
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
        
        # 查询表结构
        sql = "DESCRIBE rule_definitions"
        
        cursor.execute(sql)
        results = cursor.fetchall()
        
        print(f"\nrule_definitions表的结构:\n")
        
        for result in results:
            field_name, field_type, null, key, default, extra = result
            print(f"字段名: {field_name}")
            print(f"  类型: {field_type}")
            print(f"  允许NULL: {null}")
            print(f"  键: {key}")
            print(f"  默认值: {default}")
            print(f"  额外: {extra}")
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
    check_rule_definitions_table_structure()
