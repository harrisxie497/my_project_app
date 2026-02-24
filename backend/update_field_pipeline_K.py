"""
更新K列（輸入者住所）的field_pipelines配置中的prompt
"""

import pymysql
import json
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def update_field_pipeline():
    """更新K列（輸入者住所）的field_pipelines配置中的prompt"""
    print("=" * 100)
    print("更新K列（輸入者住所）的field_pipelines配置中的prompt")
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
        
        # 查询field_pipelines
        sql = """
        SELECT rule_params_json
        FROM field_pipelines
        WHERE file_type = 'CUSTOMS' AND target_col = 'K'
        """
        
        cursor.execute(sql)
        result = cursor.fetchone()
        
        if result:
            rule_params_json = result[0]
            print(f"\n旧的rule_params_json: {rule_params_json}")
            
            if rule_params_json and isinstance(rule_params_json, str):
                rule_params_json = json.loads(rule_params_json)
            
            # 更新prompt
            new_prompt = """你是一个专业的日英翻译专家。请将以下日文地址翻译成英文，并保持日本地址的格式。

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
12. 必须严格按顺序返回{input_count}个元素，不能多也不能少
13. 输入是数组数据，输出必须也是数组，顺序和长度与输入相同
14. 门牌号是最后一部分，后面不应该有任何信息（如"宅配ボックス希望"等）"""
            
            rule_params_json['policy_translate_from_targetcol_en_upper']['prompt'] = new_prompt
            
            print(f"\n新的prompt: {new_prompt}")
            
            # 更新数据库
            update_sql = """
            UPDATE field_pipelines
            SET rule_params_json = %s
            WHERE file_type = 'CUSTOMS' AND target_col = 'K'
            """
            
            cursor.execute(update_sql, (json.dumps(rule_params_json, ensure_ascii=False),))
            
            print("\n✅ 更新成功！")
            
            # 验证更新
            verify_sql = """
            SELECT rule_params_json
            FROM field_pipelines
            WHERE file_type = 'CUSTOMS' AND target_col = 'K'
            """
            
            cursor.execute(verify_sql)
            result = cursor.fetchone()
            
            if result and result[0]:
                rule_params_json_str = result[0]
                rule_params_json_dict = json.loads(rule_params_json_str)
                prompt = rule_params_json_dict.get('policy_translate_from_targetcol_en_upper', {}).get('prompt', '')
                print(f"\n验证 - 新的prompt前100个字符: {prompt[:100]}...")
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
    update_field_pipeline()
