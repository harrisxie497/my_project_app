#!/usr/bin/env python3
import sys
sys.path.insert(0, 'c:/Users/harris.xie/Documents/trae_projects/japan/backend')

from app.core.database import SessionLocal
from app.models.rule_definition import RuleDefinition

db = SessionLocal()
rule = db.query(RuleDefinition).filter(
    RuleDefinition.rule_ref == 'policy_ai_decimal_fix'
).first()

if rule:
    print("Current schema:")
    import json
    print(json.dumps(rule.schema_json, indent=2, ensure_ascii=False))

    print("\nUpdating rule...")
    schema = rule.schema_json
    schema['desc'] = '重量：按品名/材质/原重量进行合理修正，输出一位小数（后台固定流程）'
    schema['configurable_params']['system_prompt'] = """输入的数组数据是'材质'，'品名'，'货物重量'，我们依据数组中同位置的"材料"和"品名"来判断"货物重量"是否合理？如果合理，保留完整数值并四舍五入到一位小数（例如：输入1.234返回1.2，输入2.567返回2.6，输入0.890返回0.9），如果觉得不合理，判定为异常值（如明显偏离合理范围的数值），则可以虚拟一个合理数字，注意这个重量是一件商品的重量，单位KG，对于输出的要求，也是一个数组，并且顺序和数组长度保持输入的一样。重要说明：返回完整的一位小数数值，不要单独提取小数位。"""

    rule.schema_json = schema
    db.commit()

    print("\nNew schema:")
    print(json.dumps(rule.schema_json, indent=2, ensure_ascii=False))
    print("\nUpdate successful!")
else:
    print("Rule not found")

db.close()
