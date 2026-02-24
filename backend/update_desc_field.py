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

# 修改policy_ai_text_dress_clean的desc
sql = """
UPDATE rule_definitions
SET schema_json = JSON_SET(schema_json, '$.desc', '收件人地址（日文）格式化整理：校验门牌格式，虚拟合理门牌，保持标准地址格式（后台固定流程）')
WHERE rule_ref = 'policy_ai_text_dress_clean'
"""

cursor.execute(sql)
print(f"修改了 {cursor.rowcount} 行")

# 查询修改后的结果
sql = """
SELECT rule_ref, schema_json
FROM rule_definitions
WHERE rule_ref = 'policy_ai_text_dress_clean'
"""

cursor.execute(sql)
result = cursor.fetchone()

if result:
    rule_ref = result['rule_ref']
    schema_json = result['schema_json']
    
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
    
    desc = schema_json.get('desc', '') if isinstance(schema_json, dict) else ''
    system_prompt = schema_json.get('configurable_params', {}).get('system_prompt', '') if isinstance(schema_json, dict) else ''
    
    print("\n修改后的配置：")
    print("=" * 150)
    print(f"rule_ref: {rule_ref}")
    print(f"desc: {desc}")
    print(f"system_prompt: {system_prompt[:100] if system_prompt else ''}...")

conn.commit()
conn.close()
