#!/usr/bin/env python3
import sys
sys.path.insert(0, 'c:/Users/harris.xie/Documents/trae_projects/japan/backend')

from app.core.database import SessionLocal
from app.models.rule_definition import RuleDefinition
import json

db = SessionLocal()

# 查找CONST类型的规则
rules = db.query(RuleDefinition).filter(
    RuleDefinition.rule_type == 'CONST'
).all()

print(f"找到 {len(rules)} 个CONST类型的规则：\n")
for rule in rules:
    print(f"Rule ref: {rule.rule_ref}")
    print(f"Rule type: {rule.rule_type}")
    print(f"Executor type: {rule.executor_type}")
    print(f"Schema JSON:")
    print(json.dumps(rule.schema_json, indent=2, ensure_ascii=False))
    print("\n" + "=" * 80 + "\n")

db.close()
