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

# 更新 rule_definitions 表中的提示词
sql = '''
UPDATE rule_definitions
SET schema_json = %s
WHERE rule_ref = %s
'''

new_schema = {
    "desc": "材质：去括号备注→英译大写→材质替换表置换（后台固定流程）",
    "configurable_params": {
        "system_prompt": """你是一个专业的日英翻译专家和日本海关材料专家。请将以下日文材质进行整理并翻译。

输入格式说明：输入数据为序号列表，每行一个材质。
例如：
1. 聚酯纤维
2. 棉
3. ナイロン

处理要求：
1. 删除括号内注释（如"POLYESTER (含棉30%)"→"POLYESTER"）
2. 中文材质名按行业标准英文大写（"聚酯纤维"→"POLYESTER FIBER"）
3. 如果前后两个是重复含义，保留一个即可
4. 对于同类型的材质，可以选择税汇率较低的材质进行替换

输出格式要求（非常重要）：
1. 必须每行输出一个翻译结果
2. 不要包含序号（如"1."、"2."等）
3. 不要包含JSON格式或方括号[]
4. 只返回纯文本，每行一个材质名称
5. 输出行数必须严格等于输入行数，不能多也不能少
6. 按照输入的顺序返回结果

正确输出示例：
ABS
PLASTIC
COTTON
POLYESTER FIBER

错误输出示例（不要这样）：
1. ABS
2. PLASTIC
["ABS", "PLASTIC"]
["ABS", "PLASTIC", "COTTON", "POLYESTER FIBER"]"""
    }
}

cursor.execute(sql, (json.dumps(new_schema, ensure_ascii=False), 'policy_ai_material_en'))
conn.commit()

print('已更新 policy_ai_material_en 的提示词配置')

# 查询验证
sql = '''
SELECT rule_ref, schema_json
FROM rule_definitions
WHERE rule_ref = %s
'''
cursor.execute(sql, ('policy_ai_material_en',))
result = cursor.fetchone()

if result:
    rule_ref, schema_json = result
    print(f'\n=== 验证更新结果 ===')
    print(f'rule_ref: {rule_ref}')
    if isinstance(schema_json, str):
        schema_json = json.loads(schema_json)
    configurable_params = schema_json.get('configurable_params', {})
    system_prompt = configurable_params.get('system_prompt', '')
    print(f'\nsystem_preview: {system_prompt[:300]}...')

cursor.close()
conn.close()
