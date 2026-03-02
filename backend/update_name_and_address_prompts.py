"""
更新日本人名和日本地址的提示词
"""

import sys
import os
import pymysql
import json

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def update_prompts():
    """更新日本人名和日本地址的提示词"""
    print("=" * 100)
    print("更新日本人名和日本地址的提示词")
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
        
        # 更新 policy_ai_text_ja_clean（日本人名清理）
        print("\n" + "=" * 100)
        print("更新 policy_ai_text_ja_clean（日本人名清理）")
        print("=" * 100)
        
        ja_clean_system_prompt = """你是一个日本海关资料审核专家，你需要整理日文收件人名是否符合日本人名格式。

要求：
1. 移除敬语和称谓（様、様、先生、様方等）
2. 去掉假名（平假名/片假名），把括号以及括号内的内容去掉
3. 如果有多个名字，只保留第一个
4. 如果明显不是日本人名（例如：公司名，中文名，英文名，地址名），请虚构一个日本人名。

虚构日本人名时请遵守以下规则：
- 使用常见的日本姓氏（如：佐藤、鈴木、高橋、田中、伊藤、渡辺、山本、中村、小林、加藤等）
- 使用常见的日本名字（如：太郎、花子、健一、美咲、大輔、由美、翔太、麻衣、拓也、優子等）
- 姓氏和名字之间用空格分隔（如：佐藤 太郎）
- 每次生成时请使用不同的姓氏和名字组合，避免重复
- 如果同一批次中有多个需要虚构的名字，请确保它们互不相同

请严格遵守以下规则：
1. 输入数据是一个 JSON 数组，数组每个对象有字段"index"和"context"。
你需要处理的是context里面的内容，处理完成之后，输出同样长度的JSON 数组，index保持不变，context为处理之后的值。

例如输入：
[
  {"index": "1", "context": "Raj Merani"},
  {"index": "2", "context": "SOJIRO TSUJIMOTO"},
  ...
]
例如输出：
[
  {"index": "1", "context": "佐藤 太郎"},
  {"index": "2", "context": "鈴木 花子"},
  ...
]

2. 输出数组的长度必须严格等于输入数组的长度。
3. 不允许删除、合并、省略任何输入行，只允许修改指定字段的内容。
4. 不要添加任何额外的解释、前言或后记。"""
        
        # 查询当前的 schema_json
        sql = """
        SELECT schema_json
        FROM rule_definitions
        WHERE rule_ref = 'policy_ai_text_ja_clean'
        """
        cursor.execute(sql)
        result = cursor.fetchone()
        
        if result:
            schema_json = result[0]
            if isinstance(schema_json, str):
                schema_json = json.loads(schema_json)
            
            print(f"\n当前 schema_json: {schema_json}")
            
            # 更新 system_prompt
            schema_json['configurable_params']['system_prompt'] = ja_clean_system_prompt
            
            # 更新数据库
            update_sql = """
            UPDATE rule_definitions
            SET schema_json = %s
            WHERE rule_ref = 'policy_ai_text_ja_clean'
            """
            cursor.execute(update_sql, (json.dumps(schema_json, ensure_ascii=False),))
            connection.commit()
            
            print(f"\n✅ policy_ai_text_ja_clean 已更新")
        else:
            print(f"\n❌ 未找到 policy_ai_text_ja_clean")
        
        # 更新 policy_ai_text_dress_clean（日本地址清理）
        print("\n" + "=" * 100)
        print("更新 policy_ai_text_dress_clean（日本地址清理）")
        print("=" * 100)
        
        dress_clean_system_prompt = """你是一个日本海关资料审核专家，你需要整理日文收件人地址是否符合日本地址格式。

要求：
1. 日本地址地址层级完整的是，都道府县 → 市/区 → 町/地区 → 丁目/番地，最后的一定是丁目和番地。
2. 你需要整理地址，并且都道府县和市/区之间用空格隔开，其他层级之间也用空格隔开。
3. 如果地址中不包含丁目和番地，你需要随机虚构一个常见的门牌号码，例如：1-1-1；门牌号码左右和中间都不用保留空格。
4. 保留丁目和番号后面的建筑名称和房间号（如"CORE高梨one 201号室"、"マンション101号室"等），不要删除这些信息。
5. 建筑名称和房间号与门牌号之间用空格分隔（如"20-11 CORE高梨one 201号室"）。

请严格遵守以下规则：
1. 输入数据是一个 JSON 数组，数组每个对象有字段"index"和"context"。
你需要处理的是context里面的内容，处理完成之后，输出同样长度的JSON 数组，index保持不变，context为处理之后的值。

例如输入：
[
  {"index": "1", "context": "沖縄県 糸満市 字糸満 ２２５２番地"},
  {"index": "2", "context": "長崎県 佐世保市高梨町 20-11 CORE高梨one 201号室"},
  ...
]
例如输出：
[
  {"index": "1", "context": "沖縄県糸満市字糸満2252-1"},
  {"index": "2", "context": "長崎県佐世保市高梨町20-11 CORE高梨one 201号室"},
  ...
]

2. 输出数组的长度必须严格等于输入数组的长度。
3. 不允许删除、合并、省略任何输入行，只允许修改指定字段的内容。
4. 不要添加任何额外的解释、前言或后记。"""
        
        # 查询当前的 schema_json
        sql = """
        SELECT schema_json
        FROM rule_definitions
        WHERE rule_ref = 'policy_ai_text_dress_clean'
        """
        cursor.execute(sql)
        result = cursor.fetchone()
        
        if result:
            schema_json = result[0]
            if isinstance(schema_json, str):
                schema_json = json.loads(schema_json)
            
            print(f"\n当前 schema_json: {schema_json}")
            
            # 更新 system_prompt
            schema_json['configurable_params']['system_prompt'] = dress_clean_system_prompt
            
            # 更新数据库
            update_sql = """
            UPDATE rule_definitions
            SET schema_json = %s
            WHERE rule_ref = 'policy_ai_text_dress_clean'
            """
            cursor.execute(update_sql, (json.dumps(schema_json, ensure_ascii=False),))
            connection.commit()
            
            print(f"\n✅ policy_ai_text_dress_clean 已更新")
        else:
            print(f"\n❌ 未找到 policy_ai_text_dress_clean")
        
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
    update_prompts()
