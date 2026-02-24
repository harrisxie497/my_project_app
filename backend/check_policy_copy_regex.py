"""
检查policy_copy_regex规则的配置
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.core.database import SessionLocal
from app.models.rule_definition import RuleDefinition

def check_policy_copy_regex():
    """检查policy_copy_regex规则"""
    print("=" * 100)
    print("检查policy_copy_regex规则")
    print("=" * 100)
    
    db_session = SessionLocal()
    
    try:
        # 查询policy_copy_regex规则
        rule = db_session.query(RuleDefinition).filter(
            RuleDefinition.rule_ref == 'policy_copy_regex'
        ).first()
        
        if rule:
            print(f"\npolicy_copy_regex规则:")
            print(f"  rule_ref: {rule.rule_ref}")
            print(f"  rule_name: {rule.rule_type}")
            print(f"  schema_json: {rule.schema_json}")
        else:
            print(f"\n未找到policy_copy_regex规则")
    
    except Exception as e:
        print(f"查询失败: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        db_session.close()
    
    print("\n" + "=" * 100)
    print("检查完成")
    print("=" * 100)

if __name__ == "__main__":
    check_policy_copy_regex()
