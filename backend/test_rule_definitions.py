"""
查看rule_definitions表中的schema_json
"""

from app.core.database import SessionLocal
from app.models.rule_definition import RuleDefinition
import logging
import json

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def test_rule_definitions():
    """查看rule_definitions表中的schema_json"""
    print("=" * 100)
    print("查看rule_definitions表中的schema_json")
    print("=" * 100)
    
    db_session = SessionLocal()
    try:
        rule_definitions = db_session.query(RuleDefinition).all()
        
        print(f"\n获取到 {len(rule_definitions)} 个规则定义\n")
        
        for rule in rule_definitions:
            print(f"规则: {rule.rule_ref}")
            print(f"  rule_type: {rule.rule_type}")
            print(f"  executor_type: {rule.executor_type}")
            print(f"  schema_json:")
            if rule.schema_json:
                schema = rule.schema_json
                print(f"    {json.dumps(schema, ensure_ascii=False, indent=6)}")
            else:
                print(f"    None")
            print()
        
    except Exception as e:
        print(f"\n测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        db_session.close()


if __name__ == "__main__":
    test_rule_definitions()
