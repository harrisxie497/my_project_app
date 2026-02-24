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

# 查询所有AI列的配置
sql = """
SELECT target_col, target_header, rule_ref, rule_params_json
FROM field_pipelines
WHERE file_type = 'CUSTOMS' AND field_type = 'AI'
"""

cursor.execute(sql)
results = cursor.fetchall()

print("field_pipelines 表中AI列的配置：")
print("=" * 150)
for row in results:
    target_col = row['target_col']
    target_header = row['target_header']
    rule_ref = row['rule_ref']
    rule_params_json = row['rule_params_json']
    
    print(f"target_col: {target_col}")
    print(f"target_header: {target_header}")
    print(f"rule_ref: {rule_ref}")
    print(f"rule_params_json: {rule_params_json}")
    
    # 解析rule_params_json
    if rule_params_json:
        try:
            if isinstance(rule_params_json, str):
                rule_params_dict = json.loads(rule_params_json)
            else:
                rule_params_dict = rule_params_json
            
            # 检查是否为空字典
            if isinstance(rule_params_dict, dict):
                if not rule_params_dict:
                    print("rule_params_json 是空字典，可以置空")
                else:
                    print(f"rule_params_json 包含的键: {list(rule_params_dict.keys())}")
        except json.JSONDecodeError as e:
            print(f"解析rule_params_json失败: {e}")
    else:
        print("rule_params_json 为空")
    
    print()

conn.close()
