"""
查询Y列（收件人地址）的提示词配置
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.core.database import SessionLocal
from app.models.rule_definition import RuleDefinition

def check_y_column_prompt():
    """查询Y列的提示词配置"""
    print("=" * 100)
    print("查询Y列（收件人地址）的提示词配置")
    print("=" * 100)
    
    db_session = SessionLocal()
    
    try:
        # 查询Y列的规则定义
        rule = db_session.query(RuleDefinition).filter(
            RuleDefinition.rule_ref == 'policy_ai_text_dress_clean'
        ).first()
        
        if rule:
            print(f"\n规则引用: {rule.rule_ref}")
            print(f"规则类型: {rule.rule_type}")
            print(f"执行器类型: {rule.executor_type}")
            print(f"\n提示词:")
            print(rule.schema_json)
        else:
            print("\n未找到Y列的规则定义")
    
    finally:
        db_session.close()
    
    print("\n" + "=" * 100)
    print("查询完成")
    print("=" * 100)

if __name__ == "__main__":
    check_y_column_prompt()
