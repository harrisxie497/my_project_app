#!/usr/bin/env python3
"""
更新F列的系统提示词为保留一位小数
"""

from app.core.database import SessionLocal
from app.models.rule_definition import RuleDefinition

def update_f_column_system_prompt():
    """更新F列的系统提示词"""
    db = SessionLocal()
    try:
        # 查找F列使用的规则
        rule = db.query(RuleDefinition).filter(
            RuleDefinition.rule_ref == 'weight_extract_clean'
        ).first()

        if rule:
            # 更新系统提示词为保留一位小数
            schema = rule.schema_json
            schema['system_prompt'] = """你是专业的数据清洗专家。

你的任务是从给定的输入中提取并标准化重量信息。

输入格式：
- 材质数组（如：COTTON, POLYESTER, SILK）
- 品名数组（如：TOY, FABRIC, DRESS）
- 重量数组（如：1.234kg, 2.567kg, 0.890kg）

处理规则：
1. 从重量数组中提取数值
2. 保留完整数值并四舍五入到一位小数
   - 输入1.234kg -> 输出1.2
   - 输入2.567kg -> 输出2.6
   - 输入0.890kg -> 输出0.9
   - 输入5.500kg -> 输出5.5
3. 去除所有单位和多余字符
4. 如果输入为空或格式错误，返回空字符串

输出格式：
- 每行一个结果
- 只输出数值（如：1.2）
- 不要包含序号、单位或其他文字"""

            rule.schema_json = schema
            db.commit()
            print(f"Success: Updated rule 'weight_extract_clean' system prompt")
            print(f"\nNew system prompt:")
            print(schema['system_prompt'])
        else:
            print(f"Error: Rule 'weight_extract_clean' not found")

    except Exception as e:
        db.rollback()
        print(f"Error: Update failed - {e}")
    finally:
        db.close()

if __name__ == "__main__":
    update_f_column_system_prompt()
