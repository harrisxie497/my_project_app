import pymysql

conn = pymysql.connect(
    host='172.18.207.224',
    user='app',
    password='app123456',
    database='demo',
    charset='utf8mb4'
)

cursor = conn.cursor()

# 1. 品名翻译（policy_ai_goods_en）
sql1 = """
UPDATE rule_definitions
SET schema_json = JSON_MERGE_PATCH(
    schema_json,
    JSON_OBJECT('system_prompt', '你是一个专业的日英翻译专家。请将以下日文品名翻译成英文。要求：1. 翻译要准确、专业 2. 不要包含特殊字符（/、\等） 3. 长度不超过60个字符 4. 只返回翻译结果，不要包含其他文字。请严格遵守以下规则：1. 输出必须是合法的 JSON 数组。 2. 输出数组的长度必须严格等于输入数组的长度。 3. 不允许删除、合并、省略任何输入行，只允许修改指定字段的内容。 4. 不要添加任何额外的解释、前言或后记。')
WHERE rule_ref = 'policy_ai_goods_en'
"""

cursor.execute(sql1)
print("已执行：品名翻译（policy_ai_goods_en）")

# 2. 材质翻译（policy_ai_material_en）
sql2 = """
UPDATE rule_definitions
SET schema_json = JSON_MERGE_PATCH(
    schema_json,
    JSON_OBJECT('system_prompt', '你是一个专业的日英翻译专家。请将以下日文材质翻译成英文。要求：1. 翻译要准确、专业 2. 转换为标准材质代码（如：COTTON、POLYESTER等） 3. 只返回翻译结果，不要包含其他文字。请严格遵守以下规则：1. 输出必须是合法的 JSON 数组。 2. 输出数组的长度必须严格等于输入数组的长度。 3. 不允许删除、合并、省略任何输入行，只允许修改指定字段的内容。 4. 不要添加任何额外的解释、前言或后记。')
WHERE rule_ref = 'policy_ai_material_en'
"""

cursor.execute(sql2)
print("已执行：材质翻译（policy_ai_material_en）")

# 3. 收件人名清理（policy_ai_text_ja_clean）
sql3 = """
UPDATE rule_definitions
SET schema_json = JSON_MERGE_PATCH(
    schema_json,
    JSON_OBJECT('system_prompt', '你是一个日文数据处理专家。请清理以下日文收件人名。要求：1. 移除敬语和称谓（様、様、先生、様方等） 2. 标准化假名（平假名/片假名） 3. 长度不超过40个字符 4. 只返回清理后的名字，不要包含其他文字。请严格遵守以下规则：1. 输出必须是合法的 JSON 数组。 2. 输出数组的长度必须严格等于输入数组的长度。 3. 不允许删除、合并、省略任何输入行，只允许修改指定字段的内容。 4. 不要添加任何额外的解释、前言或后记。')
WHERE rule_ref = 'policy_ai_text_ja_clean'
"""

cursor.execute(sql3)
print("已执行：收件人名清理（policy_ai_text_ja_clean）")

# 4. 收件人地址清理（policy_ai_text_dress_clean）
sql4 = """
UPDATE rule_definitions
SET schema_json = JSON_MERGE_PATCH(
    schema_json,
    JSON_OBJECT('system_prompt', '你是一个日文数据处理专家。请清理以下日文收件人地址。要求：1. 移除敬语和称谓（様、様、先生、様方等） 2. 标准化假名（平假名/片假名） 3. 长度不超过60个字符 4. 只返回清理后的地址，不要包含其他文字。请严格遵守以下规则：1. 输出必须是合法的 JSON 数组。 2. 输出数组的长度必须严格等于输入数组的长度。 3. 不允许删除、合并、省略任何输入行，只允许修改指定字段的内容。 4. 不要添加任何额外的解释、前言或后记。')
WHERE rule_ref = 'policy_ai_text_dress_clean'
"""

cursor.execute(sql4)
print("已执行：收件人地址清理（policy_ai_text_dress_clean）")

# 5. 从目标列翻译并转大写（policy_translate_from_targetcol_en_upper）
sql5 = """
UPDATE rule_definitions
SET schema_json = JSON_MERGE_PATCH(
    schema_json,
    JSON_OBJECT('system_prompt', '你是一个专业的日英翻译专家。请将以下日文翻译成英文。要求：1. 翻译要准确、专业 2. 转换为大写 3. 长度不超过60个字符 4. 只返回翻译结果，不要包含其他文字。请严格遵守以下规则：1. 输出必须是合法的 JSON 数组。 2. 输出数组的长度必须严格等于输入数组的长度。 3. 不允许删除、合并、省略任何输入行，只允许修改指定字段的内容。 4. 不要添加任何额外的解释、前言或后记。')
WHERE rule_ref = 'policy_translate_from_targetcol_en_upper'
"""

cursor.execute(sql5)
print("已执行：从目标列翻译并转大写（policy_translate_from_targetcol_en_upper）")

# 6. 日文人名翻译为英文并大写（policy_translate_name_en_upper）
sql6 = """
UPDATE rule_definitions
SET schema_json = JSON_MERGE_PATCH(
    schema_json,
    JSON_OBJECT('system_prompt', '你是一个专业的日英翻译专家。请将以下日文人名翻译成英文。要求：1. 翻译要准确、专业 2. 转换为大写 3. 长度不超过60个字符 4. 只返回翻译结果，不要包含其他文字。请严格遵守以下规则：1. 输出必须是合法的 JSON 数组。 2. 输出数组的长度必须严格等于输入数组的长度。 3. 不允许删除、合并、省略任何输入行，只允许修改指定字段的内容。 4. 不要添加任何额外的解释、前言或后记。')
WHERE rule_ref = 'policy_translate_name_en_upper'
"""

cursor.execute(sql6)
print("已执行：日文人名翻译为英文并大写（policy_translate_name_en_upper）")

conn.commit()
conn.close()

print("所有SQL执行完成！")
