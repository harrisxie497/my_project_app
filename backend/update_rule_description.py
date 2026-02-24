#!/usr/bin/env python3
"""
更新规则描述：说明空值返回空字符串
"""

import sys
sys.path.insert(0, 'c:/Users/harris.xie/Documents/trae_projects/japan/backend')

from app.core.database import SessionLocal
from app.models.rule_definition import RuleDefinition

db = SessionLocal()

try:
    # 查找规则
    rule = db.query(RuleDefinition).filter(
        RuleDefinition.rule_ref == 'policy_copy_one_decimal'
    ).first()

    if rule:
        # 更新描述
        rule.schema_json['desc'] = "复制源值：保留1位小数，去掉非数字和小数点的字符；空值返回空字符串"

        db.commit()

        print("规则描述更新成功！")
        print(f"\n新描述: {rule.schema_json['desc']}")
    else:
        print("未找到规则 policy_copy_one_decimal")

except Exception as e:
    db.rollback()
    print(f"更新失败: {e}")
    import traceback
    traceback.print_exc()
finally:
    db.close()
