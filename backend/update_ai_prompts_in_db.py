"""
更新数据库中AI规则的提示词
"""

import pymysql
import json
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def update_ai_prompts_in_db():
    """更新数据库中AI规则的提示词"""
    print("=" * 100)
    print("更新数据库中AI规则的提示词")
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
        
        # H列（品名）的提示词
        h_prompt = """你是一个专业的日英翻译专家。请将以下日文品名翻译成英文。

要求：
1. 翻译要准确、专业
2. 不要包含特殊字符（/、\等）
3. 长度不超过60个字符
4. 每行一个翻译结果，按顺序对应
5. 只返回翻译结果，不要包含序号（如"1."、"2."等）
6. 只返回翻译结果，不要包含其他文字
7. 输入有{input_count}个元素，输出必须保持{input_count}个元素，不要偷懒输出
8. 如果某个元素无法翻译，请返回空字符串，不要跳过该元素
9. 必须严格按顺序返回{input_count}个元素，不能多也不能少"""
        
        # I列（材质）的提示词
        i_prompt = """你是一个专业的日英翻译专家。请将以下日文材质翻译成英文。

要求：
1. 翻译要准确、专业
2. 转换为标准材质代码（如：COTTON、POLYESTER等）
3. 每行一个翻译结果，按顺序对应
4. 只返回翻译结果，不要包含序号（如"1."、"2."等）
5. 只返回翻译结果，不要包含其他文字
6. 输入有{input_count}个元素，输出必须保持{input_count}个元素，不要偷懒输出
7. 如果某个元素无法翻译，请返回空字符串，不要跳过该元素
8. 必须严格按顺序返回{input_count}个元素，不能多也不能少"""
        
        # X列（收件人名（日文））的提示词
        x_prompt = """你是一个日文数据处理专家。请清理以下日文收件人名。

要求：
1. 移除敬语和称谓（様、様、先生、様方等）
2. 标准化假名（平假名/片假名）
3. 长度不超过40个字符
4. 每行一个清理结果，按顺序对应
5. 只返回清理后的名字，不要包含序号（如"1."、"2."等）
6. 只返回清理后的名字，不要包含其他文字
7. 输入有{input_count}个元素，输出必须保持{input_count}个元素，不要偷懒输出
8. 如果某个元素无法清理，请返回空字符串，不要跳过该元素
9. 必须严格按顺序返回{input_count}个元素，不能多也不能少"""
        
        # Y列（收件人地址）的提示词
        y_prompt = """请将以下日文地址格式化，保持日文格式，不要翻译成英文。

要求：
1. 地址层级完整：都道府县 → 市/区 → 町/地区 → 丁目/番地
2. 例如："愛知県名古屋市中区1-2-3" 应格式化为 "愛知県名古屋市中区1-2-3"
3. 例如："東京都渋谷区渋谷1-2-3" 应格式化为 "東京都渋谷区渋谷1-2-3"
4. 例如："大阪府大阪市中央区1-2-3" 应格式化为 "大阪府大阪市中央区1-2-3"
5. 中间不需要加标点符号，只加入空格分隔各层级
6. 门牌部分（如1-2-3）保持原格式，-两边都不需要有空格
7. 保持日文格式，不要翻译成英文（罗马字）
8. 只返回格式化后的地址，每行一个，按顺序对应，不要包含JSON格式、序号或其他文字
9. 输入有{input_count}个元素，输出必须保持{input_count}个元素，不要偷懒输出
10. 如果某个元素无法格式化，请返回空字符串，不要跳过该元素
11. 必须严格按顺序返回{input_count}个元素，不能多也不能少"""
        
        # K列（輸入者住所）的提示词
        k_prompt = """你是一个专业的日英翻译专家。请将以下日文翻译成英文。

要求：
1. 翻译要准确、专业
2. 每行一个翻译结果，按顺序对应
3. 只返回翻译结果，不要包含序号（如"1."、"2."等）
4. 只返回翻译结果，不要包含其他文字
5. 输入有{input_count}个元素，输出必须保持{input_count}个元素，不要偷懒输出
6. 如果某个元素无法翻译，请返回空字符串，不要跳过该元素
7. 必须严格按顺序返回{input_count}个元素，不能多也不能少"""
        
        # J列（輸入者名）的提示词
        j_prompt = """你是一个专业的日英翻译专家。请将以下日文翻译成英文。

要求：
1. 翻译要准确、专业
2. 每行一个翻译结果，按顺序对应
3. 只返回翻译结果，不要包含序号（如"1."、"2."等）
4. 只返回翻译结果，不要包含其他文字
5. 输入有{input_count}个元素，输出必须保持{input_count}个元素，不要偷懒输出
6. 如果某个元素无法翻译，请返回空字符串，不要跳过该元素
7. 必须严格按顺序返回{input_count}个元素，不能多也不能少"""
        
        # 更新H列（品名）的提示词
        sql = """
        UPDATE field_pipelines
        SET rule_params_json = %s
        WHERE file_type = 'CUSTOMS' AND target_col = 'H'
        """
        cursor.execute(sql, (json.dumps({"policy_ai_goods_en": {"prompt": h_prompt}}),))
        print(f"\n✅ 更新H列（品名）的提示词")
        
        # 更新I列（材质）的提示词
        sql = """
        UPDATE field_pipelines
        SET rule_params_json = %s
        WHERE file_type = 'CUSTOMS' AND target_col = 'I'
        """
        cursor.execute(sql, (json.dumps({"policy_ai_material_en": {"prompt": i_prompt}}),))
        print(f"✅ 更新I列（材质）的提示词")
        
        # 更新X列（收件人名（日文））的提示词
        sql = """
        UPDATE field_pipelines
        SET rule_params_json = %s
        WHERE file_type = 'CUSTOMS' AND target_col = 'X'
        """
        cursor.execute(sql, (json.dumps({"policy_ai_text_ja_clean": {"prompt": x_prompt}}),))
        print(f"✅ 更新X列（收件人名（日文））的提示词")
        
        # 更新Y列（收件人地址）的提示词
        sql = """
        UPDATE field_pipelines
        SET rule_params_json = %s
        WHERE file_type = 'CUSTOMS' AND target_col = 'Y'
        """
        cursor.execute(sql, (json.dumps({"policy_ai_text_dress_clean": {"prompt": y_prompt}}),))
        print(f"✅ 更新Y列（收件人地址）的提示词")
        
        # 更新K列（輸入者住所）的提示词
        sql = """
        UPDATE field_pipelines
        SET rule_params_json = %s
        WHERE file_type = 'CUSTOMS' AND target_col = 'K'
        """
        cursor.execute(sql, (json.dumps({"policy_translate_from_targetcol_en_upper": {"prompt": k_prompt}}),))
        print(f"✅ 更新K列（輸入者住所）的提示词")
        
        # 更新J列（輸入者名）的提示词
        sql = """
        UPDATE field_pipelines
        SET rule_params_json = %s
        WHERE file_type = 'CUSTOMS' AND target_col = 'J'
        """
        cursor.execute(sql, (json.dumps({"policy_translate_from_targetcol_en_upper": {"prompt": j_prompt}}),))
        print(f"✅ 更新J列（輸入者名）的提示词")
        
        # 提交事务
        connection.commit()
        
        # 查询更新后的配置
        sql = """
        SELECT target_col, target_header, rule_ref, rule_params_json
        FROM field_pipelines
        WHERE file_type = 'CUSTOMS' AND target_col IN ('H', 'I', 'X', 'Y', 'K', 'J')
        """
        
        cursor.execute(sql)
        results = cursor.fetchall()
        
        print(f"\n查询更新后的配置:")
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
        print("更新完成！")
        print("=" * 100)
        
    except Exception as e:
        print(f"\n❌ 更新失败: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    update_ai_prompts_in_db()
