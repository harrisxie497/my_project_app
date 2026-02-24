"""
执行 SQL 文件回退数据库配置
"""

import pymysql

# 数据库配置
DB_CONFIG = {
    'host': '172.18.207.224',
    'port': 3306,
    'user': 'app',
    'password': 'app123456',
    'database': 'demo',
    'charset': 'utf8mb4'
}

# 清空所有系统提示词的 SQL 语句
CLEAR_PROMPTS_SQL = """
UPDATE rule_definitions
SET schema_json = JSON_REMOVE(schema_json, '$.configurable_params.system_prompt')
WHERE rule_ref IN (
    'policy_ai_goods_en',
    'policy_ai_material_en',
    'policy_ai_text_ja_clean',
    'policy_ai_text_dress_clean',
    'policy_translate_from_targetcol_en_upper',
    'policy_translate_name_en_upper'
)
"""

def clear_system_prompts():
    """清空所有系统提示词"""
    try:
        connection = pymysql.connect(**DB_CONFIG)
        cursor = connection.cursor()
        
        cursor.execute(CLEAR_PROMPTS_SQL)
        connection.commit()
        
        affected_rows = cursor.rowcount
        cursor.close()
        connection.close()
        
        print(f"✓ 清空系统提示词成功，影响行数: {affected_rows}")
        return True
        
    except Exception as e:
        print(f"✗ 清空系统提示词失败: {str(e)}")
        return False

if __name__ == '__main__':
    print("=" * 100)
    print("开始回退数据库配置（清空系统提示词）")
    print("=" * 100)
    print()
    
    clear_system_prompts()
    
    print()
    print("=" * 100)
    print("回退完成")
    print("=" * 100)
