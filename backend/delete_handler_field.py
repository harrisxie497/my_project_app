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

# 查询所有AI规则的定义
sql = """
SELECT rule_ref, schema_json
FROM rule_definitions
WHERE rule_ref IN (
    'policy_ai_goods_en',
    'policy_ai_material_en',
    'policy_translate_name_en_upper',
    'policy_translate_from_targetcol_en_upper',
    'policy_ai_text_ja_clean',
    'policy_ai_text_dress_clean'
)
"""

cursor.execute(sql)
results = cursor.fetchall()

print("修改前的配置：")
print("=" * 150)
for row in results:
    rule_ref = row['rule_ref']
    schema_json = row['schema_json']
    
    # 解析schema_json
    if isinstance(schema_json, str):
        try:
            # 第一次解析
            schema_json = json.loads(schema_json)
            # 如果解析后仍然是字符串，则进行第二次解析
            if isinstance(schema_json, str):
                schema_json = json.loads(schema_json)
        except json.JSONDecodeError as e:
            print(f"解析schema_json失败: {e}")
            continue
    
    handler = schema_json.get('handler', '') if isinstance(schema_json, dict) else ''
    
    print(f"rule_ref: {rule_ref}")
    print(f"handler: {handler}")
    print()

# 删除handler字段
for row in results:
    rule_ref = row['rule_ref']
    schema_json = row['schema_json']
    
    # 解析schema_json
    if isinstance(schema_json, str):
        try:
            # 第一次解析
            schema_json = json.loads(schema_json)
            # 如果解析后仍然是字符串，则进行第二次解析
            if isinstance(schema_json, str):
                schema_json = json.loads(schema_json)
        except json.JSONDecodeError as e:
            print(f"解析schema_json失败: {e}")
            continue
    
    # 删除handler字段
    if isinstance(schema_json, dict) and 'handler' in schema_json:
        del schema_json['handler']
        
        # 更新数据库
        update_sql = """
        UPDATE rule_definitions
        SET schema_json = %s
        WHERE rule_ref = %s
        """
        
        cursor.execute(update_sql, (json.dumps(schema_json, ensure_ascii=False), rule_ref))
        print(f"已删除 {rule_ref} 的handler字段")

conn.commit()

# 查询修改后的结果
cursor.execute(sql)
results = cursor.fetchall()

print("\n修改后的配置：")
print("=" * 150)
for row in results:
    rule_ref = row['rule_ref']
    schema_json = row['schema_json']
    
    # 解析schema_json
    if isinstance(schema_json, str):
        try:
            # 第一次解析
            schema_json = json.loads(schema_json)
            # 如果解析后仍然是字符串，则进行第二次解析
            if isinstance(schema_json, str):
                schema_json = json.loads(schema_json)
        except json.JSONDecodeError as e:
            print(f"解析schema_json失败: {e}")
            continue
    
    handler = schema_json.get('handler', '') if isinstance(schema_json, dict) else ''
    
    print(f"rule_ref: {rule_ref}")
    print(f"handler: {handler}")
    print()

conn.close()
