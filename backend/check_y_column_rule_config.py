"""
检查Y列的规则配置
"""

import pymysql

def check_y_column_rule_config():
    """检查Y列的规则配置"""
    print("=" * 100)
    print("检查Y列的规则配置")
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
        
        # 查询Y列的规则配置
        sql = """
        SELECT rule_ref, system_prompt, target_col
        FROM rule_definitions
        WHERE rule_ref = 'policy_ai_text_dress_clean'
        """
        
        cursor.execute(sql)
        results = cursor.fetchall()
        
        print(f"\n找到 {len(results)} 个规则配置:\n")
        
        for result in results:
            rule_ref, system_prompt, target_col = result
            
            print(f"规则引用: {rule_ref}")
            print(f"目标列: {target_col}")
            print(f"系统提示词: {system_prompt}")
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
    check_y_column_rule_config()
