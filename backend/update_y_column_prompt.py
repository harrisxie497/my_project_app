"""
更新Y列（收件人地址）的AI系统提示词
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.core.database import SessionLocal
from app.models.rule_definition import RuleDefinition
import json

def update_y_column_prompt():
    """更新Y列的AI系统提示词"""
    print("=" * 100)
    print("更新Y列（收件人地址）的AI系统提示词")
    print("=" * 100)
    
    db_session = SessionLocal()
    
    try:
        # 查询Y列的规则定义
        rule = db_session.query(RuleDefinition).filter(
            RuleDefinition.rule_ref == 'policy_ai_text_dress_clean'
        ).first()
        
        if rule:
            print(f"\n更新前提示词:")
            print(f"  规则引用: {rule.rule_ref}")
            print(f"  规则类型: {rule.rule_type}")
            print(f"  执行器类型: {rule.executor_type}")
            print(f"  提示词: {rule.schema_json}")
            
            # 新的系统提示词
            new_system_prompt = """你是一个日文地址整理专家，请将以下日文地址进行格式化整理并输出。
有以下要求：
1.地址的最后面需校验门牌格式，日本地址门牌格式（如"4-10-25""1-102B"），无法解析则虚拟合理门牌格式（如"1-10-25"），如果门牌号码为空，请虚构后面的门牌号码，门牌号码之间用-链接。
2.最后按照日本标准地址格式输出（如"东京都渋谷区道玄坂1-10-25"），在门牌的部分不能有空格，门牌号码后面不在有其他的信息（例如：1-10-101这种就很好， 在-两边都不需要有空格）
3.中间不需要加标点符号，原有地址输入中有空格也不需要管。
4.输入有{input_count}个元素，输出必须保持{input_count}个元素，必须严格按顺序返回{input_count}个元素，不能多也不能少。"""
            
            # 更新系统提示词
            if isinstance(rule.schema_json, str):
                schema_json = json.loads(rule.schema_json)
            else:
                schema_json = rule.schema_json
            
            schema_json['configurable_params']['system_prompt'] = new_system_prompt
            
            # 更新配置
            rule.schema_json = json.dumps(schema_json, ensure_ascii=False)
            
            print(f"\n更新后提示词:")
            print(f"  规则引用: {rule.rule_ref}")
            print(f"  规则类型: {rule.rule_type}")
            print(f"  执行器类型: {rule.executor_type}")
            print(f"  提示词: {rule.schema_json}")
            
            db_session.commit()
            print(f"\nY列提示词更新成功")
        else:
            print("\n未找到Y列的规则定义")
    
    finally:
        db_session.close()
    
    print("\n" + "=" * 100)
    print("更新完成")
    print("=" * 100)

if __name__ == "__main__":
    update_y_column_prompt()
