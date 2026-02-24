"""
更新rule_ref为"policy_translate_from_targetcol_en_upper"的system_prompt
"""

import pymysql
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def update_rule_definition():
    """更新rule_ref为"policy_translate_from_targetcol_en_upper"的system_prompt"""
    print("=" * 100)
    print("更新rule_ref为\"policy_translate_from_targetcol_en_upper\"的system_prompt")
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
        
        # 优化后的提示词
        new_system_prompt = """你是一个专业的日英翻译专家。请将以下日文地址翻译成英文，并保持日本地址的格式。

输入数据：
{输入数据}

要求：
1. 翻译要准确、专业
2. 地址层级完整：都道府县 → 市/区 → 町/地区 → 丁目/番地
3. 例如："愛知県名古屋市中区1-2-3" 应翻译为 "Aichi Ken Nagoya Shi Naka Ku 1-2-3"
4. 例如："東京都渋谷区渋谷1-2-3" 应翻译为 "Tokyo To Shibuya Ku Shibuya 1-2-3"
5. 例如："大阪府大阪市中央区1-2-3" 应翻译为 "Osaka Fu Osaka Shi Chuo Ku 1-2-3"
6. 中间不需要加标点符号，只加入空格分隔各层级
7. 门牌部分（如1-2-3）保持原格式，-两边都不需要有空格
8. 翻译结果全部大写（全大写）
9. 只返回翻译后的地址，每行一个，按顺序对应，不要包含JSON格式、序号或其他文字
10. 输入有{input_count}个元素，输出必须保持{input_count}个元素，不要偷懒输出
11. 如果某个元素无法翻译，请返回空字符串，不要跳过该元素
12. 必须严格按顺序返回{input_count}个元素，不能多也不能少"""
        
        # 使用SQL直接更新
        update_sql = """
        UPDATE rule_definitions
        SET schema_json = JSON_SET(schema_json, '$.configurable_params.system_prompt', %s)
        WHERE rule_ref = %s
        """
        
        cursor.execute(update_sql, (new_system_prompt, 'policy_translate_from_targetcol_en_upper'))
        
        print("\n✅ 更新成功！")
        
        # 验证更新
        verify_sql = """
        SELECT schema_json
        FROM rule_definitions
        WHERE rule_ref = %s
        """
        
        cursor.execute(verify_sql, ('policy_translate_from_targetcol_en_upper',))
        result = cursor.fetchone()
        
        if result and result[0]:
            schema_json_str = result[0]
            print(f"\n验证 - 新的system_prompt前100个字符: {schema_json_str[:100]}...")
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
    update_rule_definition()
