#!/usr/bin/env python3
"""
更新F列的系统提示词和描述为保留一位小数
"""

from app.core.database import SessionLocal
from app.models.rule_definition import RuleDefinition

def update_f_column_system_prompt():
    """更新F列的系统提示词"""
    db = SessionLocal()
    try:
        # 查找F列使用的规则
        rule = db.query(RuleDefinition).filter(
            RuleDefinition.rule_ref == 'policy_ai_decimal_fix'
        ).first()

        if rule:
            # 更新系统提示词和描述
            schema = rule.schema_json
            schema['desc'] = '重量：按品名/材质/原重量进行合理修正，输出一位小数（后台固定流程）'
            schema['configurable_params']['system_prompt'] = """输入的数组数据是'材质'，'品名'，'货物重量'，我们依据数组中同位置的"材料"和"品名"来判断"货物重量"是否合理？如果合理，保留完整数值并四舍五入到一位小数（例如：输入1.234返回1.2，输入2.567返回2.6，输入0.890返回0.9），如果觉得不合理，判定为异常值（如明显偏离合理范围的数值），则可以虚拟一个合理数字，注意这个重量是一件商品的重量，单位KG，对于输出的要求，也是一个数组，并且顺序和数组长度保持输入的一样。重要说明：返回完整的一位小数数值，不要单独提取小数位。"""

            rule.schema_json = schema
            db.commit()
            print(f"Success: Updated rule 'policy_ai_decimal_fix'")
            print(f"\nNew desc: {schema['desc']}")
            print(f"\nNew system prompt:")
            print(schema['configurable_params']['system_prompt'])
        else:
            print(f"Error: Rule 'policy_ai_decimal_fix' not found")

    except Exception as e:
        db.rollback()
        print(f"Error: Update failed - {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    update_f_column_system_prompt()
