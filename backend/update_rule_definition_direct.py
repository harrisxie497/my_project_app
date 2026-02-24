"""
直接在数据库中更新rule_ref为"policy_ai_text_dress_clean"的system_prompt
"""

import pymysql
import json
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def update_rule_definition_direct():
    """直接在数据库中更新system_prompt"""
    print("=" * 100)
    print("直接在数据库中更新rule_ref为\"policy_ai_text_dress_clean\"的system_prompt")
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
        
        # 查询规则定义
        sql = """
        SELECT rule_ref, rule_type, executor_type, schema_json
        FROM rule_definitions
        WHERE rule_ref = %s
        """
        
        cursor.execute(sql, ('policy_ai_text_dress_clean',))
        result = cursor.fetchone()
        
        if result:
            rule_ref, rule_type, executor_type, schema_json = result
            print(f"\nrule_ref: {rule_ref}")
            print(f"rule_type: {rule_type}")
            print(f"executor_type: {executor_type}")
            print(f"\n旧的schema_json: {schema_json}")
            
            if schema_json and isinstance(schema_json, dict):
                # 更新system_prompt
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
                
                # 更新schema_json
                schema_json['configurable_params']['system_prompt'] = new_system_prompt
                
                print(f"\n新的system_prompt: {new_system_prompt}")
                
                # 更新数据库
                update_sql = """
                UPDATE rule_definitions
                SET schema_json = %s
                WHERE rule_ref = %s
                """
                
                cursor.execute(update_sql, (json.dumps(schema_json, ensure_ascii=False), 'policy_ai_text_dress_clean'))
                connection.commit()
                
                print("\n✅ 更新成功！")
        else:
            print("\n❌ 没有找到规则定义")
        
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
    update_rule_definition_direct()
