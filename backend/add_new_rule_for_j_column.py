import pymysql
import json

conn = pymysql.connect(
    host='172.18.207.224',
    user='app',
    password='app123456',
    database='demo',
    charset='utf8mb4'
)

cursor = conn.cursor(pymysql.cursors.DictCursor)

# 1. 在rule_definitions表中添加新的rule_ref
new_rule_ref = 'policy_translate_name_en_upper'
new_schema_json = {
    "desc": "从目标列翻译为英文并大写（人名翻译）",
    "handler": "ai.translate_name_to_en_upper",
    "configurable_params": {
        "system_prompt": """你是一个专业的日英翻译专家。请将以下日文人名翻译成英文。

输入数据：
{输入数据}

要求：
1. 翻译要准确、专业
2. 姓和名之间用空格分隔
3. 翻译结果全部大写（全大写）
4. 只返回翻译后的名字，每行一个，按顺序对应
5. 不要包含序号（如"1."、"2."等）
6. 只返回翻译结果，不要包含其他文字
7. 输入有{input_count}个元素，输出必须保持{input_count}个元素，不要偷懒输出
8. 如果某个元素无法翻译，请返回空字符串，不要跳过该元素
9. 必须严格按顺序返回{input_count}个元素，不能多也不能少"""
    }
}

try:
    # 插入新的rule_ref
    cursor.execute('''
        INSERT INTO rule_definitions (rule_ref, rule_type, executor_type, schema_json, enabled, created_at, updated_at)
        VALUES (%s, %s, %s, %s, %s, NOW(), NOW())
    ''', (
        new_rule_ref,
        'AI',
        'batch',
        json.dumps(new_schema_json, ensure_ascii=False),
        1
    ))
    
    print(f"成功添加新的rule_ref: {new_rule_ref}")
    
    # 2. 更新field_pipelines表中J列的rule_ref
    cursor.execute('''
        UPDATE field_pipelines
        SET rule_ref = %s
        WHERE file_type = 'CUSTOMS' AND target_col = 'J' AND field_type = 'AI'
    ''', (f'["{new_rule_ref}"]',))
    
    print(f"成功更新J列的rule_ref为: {new_rule_ref}")
    
    conn.commit()
    print("提交成功")
    
except Exception as e:
    conn.rollback()
    print(f"操作失败: {e}")
    import traceback
    traceback.print_exc()
finally:
    conn.close()
