#!/usr/bin/env python3
"""
测试F列保留一位小数
"""

import sys
sys.path.insert(0, 'c:/Users/harris.xie/Documents/trae_projects/japan/backend')

from app.core.database import SessionLocal
from app.models.rule_definition import RuleDefinition
from app.services.ai_rule_executor import AIRuleExecutor

def test_f_column_one_decimal():
    """测试F列保留一位小数"""
    db = SessionLocal()
    try:
        # 获取规则配置
        rule = db.query(RuleDefinition).filter(
            RuleDefinition.rule_ref == 'policy_ai_decimal_fix'
        ).first()

        if not rule:
            print("Error: Rule 'policy_ai_decimal_fix' not found")
            return

        print(f"Rule ref: {rule.rule_ref}")
        print(f"Rule type: {rule.rule_type}")
        print(f"\nSystem prompt:\n{rule.schema_json.get('system_prompt', '')}")
        print("\n" + "="*80)

        # 准备测试数据 - 使用处理后的H列和I列的值
        material_list = ["COTTON", "POLYESTER", "SILK"]  # I列处理后的值
        goods_list = ["TOY", "FABRIC", "DRESS"]  # H列处理后的值
        weight_list = ["1.234", "2.567", "0.890"]  # F列原始值

        # 构建用户提示词
        user_prompt = f"""{rule.schema_json.get('desc', '')}

材质数组：
{chr(10).join(material_list)}

品名数组：
{chr(10).join(goods_list)}

重量数组：
{chr(10).join(weight_list)}

要求：
1. 输入的数组顺序保持不变
2. 每行一个结果，按顺序对应，只返回重量数值
3. 保留完整数值并四舍五入到一位小数，例如：输入1.234返回1.2，输入2.567返回2.6，输入0.890返回0.9
4. 只返回结果，不要包含序号、单位或其他文字"""

        print(f"\nUser prompt:\n{user_prompt}")
        print("\n" + "="*80)

        # 调用AI规则执行器
        executor = AIRuleExecutor()
        print("\nProcessing...")
        result = executor.execute_batch_rule(
            system_prompt=rule.schema_json.get('system_prompt', ''),
            user_prompt=user_prompt,
            batch_size=3
        )

        print("\n" + "="*80)
        print("\nResults:")
        print(f"\nInput weights: {weight_list}")
        print(f"Output result: {result}")
        print(f"\nExpected result: ['1.2', '2.6', '0.9']")

        # 验证结果
        expected = ['1.2', '2.6', '0.9']
        if result == expected:
            print("\n[SUCCESS] Test passed! F column processed correctly (1 decimal)")
        else:
            print(f"\n[FAILED] Test failed!")
            print(f"   Expected: {expected}")
            print(f"   Actual: {result}")

    except Exception as e:
        print(f"\n[FAILED] Test failed: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    test_f_column_one_decimal()
