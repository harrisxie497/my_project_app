"""
使用SQL直接更新rule_ref为"policy_ai_text_dress_clean"的system_prompt
"""

import pymysql
import json
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def update_with_sql():
    """使用SQL直接更新"""
    print("=" * 100)
    print("使用SQL直接更新rule_ref为\"policy_ai_text_dress_clean\"的system_prompt")
    print("=" * 100)
    
    try:
        connection = pymysql.connect(
            host='172.18.207.224',
            port=3306,
            user='app',
            password='app123456',
            database='demo',
            charset='utf8mb4',
            autocommit=True
        )
        cursor = connection.cursor()
        
        # 直接使用SQL更新
        new_system_prompt = """请将以下日文地址格式化，保持日文格式，不要翻译成英文。

输入数据：
{输入数据}

要求：
1. 地址层级完整：都道府县 → 市/区 → 町/地区 → 丁目/番地
2. 例如："愛知県名古屋市中区1-2-3" 应格式化为 "愛知県名古屋市中区1-2-3"
3. 例如："東京都渋谷区渋谷1-2-3" 应格式化为 "東京都渋谷区渋谷1-2-3"
4. 例如："大阪府大阪市中央区1-2-3" 应格式化为 "大阪府大阪市中央区1-2-3"
5. 中间不需要加标点符号，只加入空格分隔各层级
6. 门牌部分（如1-2-3）保持原格式，-两边都不需要有空格
7. 如果门牌号码为空，请虚构后面的门牌号码，门牌号码之间用-链接
8. 保持日文格式，不要翻译成英文（罗马字）
9. 只返回格式化后的地址，每行一个，按顺序对应，不要包含JSON格式、序号或其他文字
10. 输入有{input_count}个元素，输出必须保持{input_count}个元素，不要偷懒输出
11. 如果某个元素无法格式化，请返回空字符串，不要跳过该元素
12. 必须严格按顺序返回{input_count}个元素，不能多也不能少"""
        
        # 使用JSON函数更新
        update_sql = """
        UPDATE rule_definitions
        SET schema_json = JSON_SET(schema_json, '$.configurable_params.system_prompt', %s)
        WHERE rule_ref = %s
        """
        
        cursor.execute(update_sql, (new_system_prompt, 'policy_ai_text_dress_clean'))
        
        print("\n✅ 更新成功！")
        
        # 验证更新
        verify_sql = """
        SELECT schema_json
        FROM rule_definitions
        WHERE rule_ref = %s
        """
        
        cursor.execute(verify_sql, ('policy_ai_text_dress_clean',))
        result = cursor.fetchone()
        
        if result and result[0]:
            schema_json = json.loads(result[0])
            system_prompt = schema_json.get('configurable_params', {}).get('system_prompt', '')
            print(f"\n验证 - 新的system_prompt前100个字符: {system_prompt[:100]}...")
        else:
            print("\n❌ 验证失败")
        
        cursor.close()
        connection.close()
        
        print("\n" + "=" * 100)
        print("更新完成！")
        print("=" * 100)
        
    except Exception as e:
        print(f"\n❌ 更新失败: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    update_with_sql()
