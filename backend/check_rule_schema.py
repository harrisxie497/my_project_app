#!/usr/bin/env python3
import sys
sys.path.insert(0, 'c:/Users/harris.xie/Documents/trae_projects/japan/backend')

from app.core.database import SessionLocal
from app.models.rule_definition import RuleDefinition
import json

db = SessionLocal()
rule = db.query(RuleDefinition).filter(
    RuleDefinition.rule_ref == 'policy_ai_decimal_fix'
).first()

if rule:
    print(f"Rule ref: {rule.rule_ref}")
    print(f"\nSchema JSON:")
    print(json.dumps(rule.schema_json, indent=2, ensure_ascii=False))
db.close()
