"""
系统提示词更新脚本

此脚本将所有系统提示词更新到数据库。
直接运行此脚本即可更新数据库中的系统提示词。

使用方法：
    python update_system_prompt.py
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

# 所有系统提示词配置
SYSTEM_PROMPTS = {
    'policy_ai_goods_en': '''请严格遵守以下规则：
1. 输出必须是合法的 JSON 数组。
2. 输出数组的长度必须严格等于输入数组的长度。
3. 不允许删除、合并、省略任何输入行，只允许修改指定字段的内容。
4. 不要添加任何额外的解释、前言或后记。''',

    'policy_ai_material_en': '''请严格遵守以下规则：
1. 输出必须是合法的 JSON 数组。
2. 输出数组的长度必须严格等于输入数组的长度。
3. 不允许删除、合并、省略任何输入行，只允许修改指定字段的内容。
4. 不要添加任何额外的解释、前言或后记。''',

    'policy_ai_text_ja_clean': '''请严格遵守以下规则：
1. 输出必须是合法的 JSON 数组。
2. 输出数组的长度必须严格等于输入数组的长度。
3. 不允许删除、合并、省略任何输入行，只允许修改指定字段的内容。
4. 不要添加任何额外的解释、前言或后记。''',

    'policy_ai_text_dress_clean': '''请严格遵守以下规则：
1. 输出必须是合法的 JSON 数组。
2. 输出数组的长度必须严格等于输入数组的长度。
3. 不允许删除、合并、省略任何输入行，只允许修改指定字段的内容。
4. 不要添加任何额外的解释、前言或后记。''',

    'policy_translate_from_targetcol_en_upper': '''请严格遵守以下规则：
1. 输出必须是合法的 JSON 数组。
2. 输出数组的长度必须严格等于输入数组的长度。
3. 不允许删除、合并、省略任何输入行，只允许修改指定字段的内容。
4. 不要添加任何额外的解释、前言或后记。''',

    'policy_translate_name_en_upper': '''请严格遵守以下规则：
1. 输出必须是合法的 JSON 数组。
2. 输出数组的长度必须严格等于输入数组的长度。
3. 不允许删除、合并、省略任何输入行，只允许修改指定字段的内容。
4. 不要添加任何额外的解释、前言或后记。''',
}


def update_system_prompt(rule_ref: str, system_prompt: str) -> bool:
    """
    更新数据库中指定规则的系统提示词
    
    输入：
        rule_ref: 规则引用标识符
        system_prompt: 新的系统提示词
    
    输出：
        更新是否成功
    """
    try:
        connection = pymysql.connect(**DB_CONFIG)
        cursor = connection.cursor()
        
        sql = """
        UPDATE rule_definitions
        SET schema_json = JSON_SET(
            schema_json,
            '$.configurable_params.system_prompt',
            %s
        )
        WHERE rule_ref = %s
        """
        
        cursor.execute(sql, (system_prompt, rule_ref))
        connection.commit()
        
        affected_rows = cursor.rowcount
        cursor.close()
        connection.close()
        
        print(f"✓ 更新规则 {rule_ref} 成功，影响行数: {affected_rows}")
        return affected_rows > 0
        
    except Exception as e:
        print(f"✗ 更新规则 {rule_ref} 失败: {str(e)}")
        return False


def main():
    """主函数，更新所有系统提示词"""
    print("=" * 100)
    print("开始更新系统提示词到数据库")
    print("=" * 100)
    print()
    
    success_count = 0
    fail_count = 0
    
    for rule_ref, system_prompt in SYSTEM_PROMPTS.items():
        print(f"处理规则: {rule_ref}")
        print(f"提示词: {system_prompt[:50]}...")
        
        if update_system_prompt(rule_ref, system_prompt):
            success_count += 1
        else:
            fail_count += 1
        print()
    
    print("=" * 100)
    print(f"更新完成！成功: {success_count}, 失败: {fail_count}")
    print("=" * 100)


if __name__ == '__main__':
    main()
