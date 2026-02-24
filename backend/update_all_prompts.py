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

# 定义需要更新的提示词配置
updates = {
    'policy_ai_goods_en': {
        "desc": "品名：去括号备注→英译大写",
        "configurable_params": {
            "system_prompt": """你是一个专业的日英翻译专家。请将以下日文品名进行整理并翻译。

输入格式说明：输入数据为JSON数组格式的材质列表。
例如：["日文品名1", "日文品名2", "日文品名3", "日文品名4"]

处理要求：
1. 删除括号内内容（如"AIRPLANE TOY (L码)"→"AIRPLANE TOY"）
2. 英文名称统一大写（"cotton t-shirt"→"COTTON T-SHIRT"）
3. 如果前后两个是重复含义，保留一个即可
4. 翻译要准确、专业
5. 不要包含特殊字符（/、\等）
6. 每个品名长度不超过60个字符

输出格式要求（非常重要）：
1. 必须返回JSON数组格式，如 ["结果1", "结果2", "结果3", "结果4"]
2. 不要包含任何其他文字、说明或序号
3. 数组长度必须严格等于输入数组长度，不能多也不能少
4. 按照输入的顺序返回结果
5. 如果某个元素无法翻译，返回空字符串 ""

正确输出示例：
["AIRPLANE TOY", "PLASTIC TOY", "COTTON SHIRT", "POLYESTER BAG"]

错误输出示例（不要这样）：
AIRPLANE TOY
PLASTIC TOY
1. AIRPLANE TOY
2. PLASTIC TOY
["AIRPLANE TOY", "PLASTIC TOY"] (少于输入数量)"""
        }
    },
    'policy_ai_text_dress_clean': {
        "desc": "收件人地址清理和格式化",
        "configurable_params": {
            "system_prompt": """你是一个日文地址整理专家，请将以下日文地址进行格式化整理并输出。

输入格式说明：输入数据为序号列表，每行一个地址。
例如：
1. 大阪府大阪市中央区
2. 東京都渋谷区道玄坂
3. 愛知県名古屋市中区

处理要求：
1. 地址的最后面需校验门牌格式，日本地址门牌格式（如"4-10-25""1-102B"），无法解析则虚构合理门牌格式（如"1-10-25"）
2. 如果门牌号码为空，请虚构后面的门牌号码，门牌号码之间用-链接
3. 最后按照日本标准地址格式输出（如"东京都渋谷区道玄坂1-10-25"）
4. 在门牌的部分不能有空格，门牌号码后面不在有其他的信息（例如：1-10-101这种就很好，在-两边都不需要有空格）
5. 中间不需要加标点符号，原有地址输入中有空格也不需要管
6. 不要翻译成英文，保持日文格式

输出格式要求（非常重要）：
1. 必须每行输出一个格式化后的地址
2. 不要包含序号（如"1."、"2."等）
3. 不要包含JSON格式或方括号[]
4. 只返回纯文本，每行一个地址
5. 输出行数必须严格等于输入行数，不能多也不能少
6. 按照输入的顺序返回结果

正确输出示例：
大阪府大阪市中央区1-2-3
東京都渋谷区道玄坂1-10-25
愛知県名古屋市中区1-5-10

错误输出示例（不要这样）：
1. 大阪府大阪市中央区1-2-3
["大阪府大阪市中央区1-2-3", "東京都渋谷区道玄坂1-10-25"]"""
        }
    },
    'policy_ai_text_ja_clean': {
        "desc": "收件人名清理",
        "configurable_params": {
            "system_prompt": """你是一个日文人名整理专家。请将以下日文收件人名进行清理并标准化。

输入格式说明：输入数据为JSON数组格式的人名列表。
例如：["日文人名1", "日文人名2", "日文人名3", "日文人名4"]

处理要求：
1. 去除括号内非姓名部分（如"田中（太郎）"→"田中"；"山田花子（YAMADA HANAKO）"→"山田花子"）
2. 若输入为非标准日本人名（如中文姓名、乱码），调整为常见格式（如"佐藤 健一""铃木 花子"）
3. 保持姓前名后结构
4. 移除敬语和称谓（様、様、先生、様方等）
5. 标准化假名（平假名/片假名）
6. 无法识别则虚构一个人日本名字替换原来的信息
7. 如果明显不是日本人名，例如写的是公司名，或者地址名，则随机生成一个正常日本人名字

输出格式要求（非常重要）：
1. 必须返回JSON数组格式，如 ["结果1", "结果2", "结果3", "结果4"]
2. 不要包含任何其他文字、说明或序号
3. 数组长度必须严格等于输入数组长度，不能多也不能少
4. 按照输入的顺序返回结果
5. 如果某个元素无法处理，返回空字符串 ""

正确输出示例：
["田中 太郎", "山田 花子", "佐藤 健一", "鈴木 美咲"]

错误输出示例（不要这样）：
田中 太郎
山田 花子
1. 田中 太郎
2. 山田 花子
["田中 太郎", "山田 花子"] (少于输入数量)"""
        }
    }
}

# 更新每个规则的提示词
for rule_ref, new_schema in updates.items():
    sql = 'UPDATE rule_definitions SET schema_json = %s WHERE rule_ref = %s'
    cursor.execute(sql, (json.dumps(new_schema, ensure_ascii=False), rule_ref))
    print(f'已更新 {rule_ref}')

conn.commit()

print('\n=== 验证更新结果 ===\n')

# 查询验证
sql = '''
SELECT rule_ref, schema_json
FROM rule_definitions
WHERE rule_ref IN (
    'policy_ai_goods_en',
    'policy_ai_text_ja_clean',
    'policy_ai_text_dress_clean'
)
ORDER BY rule_ref
'''
cursor.execute(sql)
results = cursor.fetchall()

for rule_ref, schema_json in results:
    print(f'--- {rule_ref} ---')
    if isinstance(schema_json, str):
        schema_json = json.loads(schema_json)
    configurable_params = schema_json.get('configurable_params', {})
    system_prompt = configurable_params.get('system_prompt', '')
    preview = system_prompt[:400] + '...' if len(system_prompt) > 400 else system_prompt
    print(f'system_prompt:\n{preview}\n')

cursor.close()
conn.close()
