import pymysql
import json

conn = pymysql.connect(
    host='172.18.207.224',
    port=3306,
    user='app',
    password='app123456',
    database='demo',
    charset='utf8mb4'
)
cursor = conn.cursor()

# 更新 policy_ai_text_ja_clean 的提示词，修正输入格式
sql = '''
UPDATE rule_definitions
SET schema_json = %s
WHERE rule_ref = %s
'''

new_schema = {
    "desc": "收件人名清理",
    "configurable_params": {
        "system_prompt": """你是一个日文人名整理专家。请将以下日文收件人名进行清理并标准化。

输入格式说明：输入数据为序号列表，每行一个人名。
例如：
1. 田中 太郎
2. 山田花子
3. 鈴木 健一

处理要求：
1. 去除括号内非姓名部分（如"田中（太郎）"→"田中"；"山田花子（YAMADA HANAKO）"→"山田花子"）
2. 若输入为非标准日本人名（如中文姓名、乱码），调整为常见格式（如"佐藤 健一""鈴木 花子"）
3. 保持姓前名后结构
4. 移除敬语和称谓（様、様、先生、様方等）
5. 标准化假名（平假名/片假名）
6. 无法识别则虚构一个人日本名字替换原来的信息
7. 如果明显不是日本人名，例如写的是公司名，或者地址名，则随机生成一个正常日本人名字
8. 每个名字长度不超过40个字符

输出格式要求（非常重要）：
1. 必须每行输出一个清理后的名字
2. 不要包含序号（如"1."、"2."等）
3. 不要包含JSON格式或方括号[]
4. 只返回纯文本，每行一个人名
5. 输出行数必须严格等于输入行数，不能多也不能少
6. 按照输入的顺序返回结果

正确输出示例：
田中 太郎
山田 花子
佐藤 健一
鈴木 美咲

错误输出示例（不要这样）：
1. 田中 太郎
2. 山田 花子
["田中 太郎", "山田 花子"]
田中 太郎
山田 花子 (少于4行)"""
    }
}

cursor.execute(sql, (json.dumps(new_schema, ensure_ascii=False), 'policy_ai_text_ja_clean'))
conn.commit()

print('已更新 policy_ai_text_ja_clean 的提示词配置')

# 查询验证
sql = '''
SELECT rule_ref, schema_json
FROM rule_definitions
WHERE rule_ref = %s
'''
cursor.execute(sql, ('policy_ai_text_ja_clean',))
result = cursor.fetchone()

if result:
    rule_ref, schema_json = result
    print(f'\n=== 验证更新结果 ===')
    print(f'rule_ref: {rule_ref}')
    if isinstance(schema_json, str):
        schema_json = json.loads(schema_json)
    configurable_params = schema_json.get('configurable_params', {})
    system_prompt = configurable_params.get('system_prompt', '')
    preview = system_prompt[:400] + '...' if len(system_prompt) > 400 else system_prompt
    print(f'\nsystem_prompt:\n{preview}')

cursor.close()
conn.close()
