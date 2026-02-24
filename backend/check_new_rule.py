#!/usr/bin/env python3
import sys
sys.path.insert(0, 'c:/Users/harris.xie/Documents/trae_projects/japan/backend')

from app.core.database import SessionLocal
from app.models.rule_definition import RuleDefinition
import json

db = SessionLocal()

# 查找新规则
rule = db.query(RuleDefinition).filter(
    RuleDefinition.rule_ref == 'policy_copy_one_decimal'
).first()

if rule:
    print("新规则验证成功：")
    print(f"  rule_ref: {rule.rule_ref}")
    print(f"  rule_type: {rule.rule_type}")
    print(f"  executor_type: {rule.executor_type}")
    print(f"  enabled: {rule.enabled}")
    print(f"\nSchema JSON:")
    print(json.dumps(rule.schema_json, indent=2, ensure_ascii=False))
else:
    print("未找到 policy_copy_one_decimal 规则")

db.close()
