"""
检查DELIVERY的FieldPipeline中引用的rule_definitions
"""
from app.core.database import SessionLocal
from app.models.field_pipeline import FieldPipeline
from app.models.rule_definition import RuleDefinition
import json

print("=" * 80)
print("检查DELIVERY的FieldPipeline和RuleDefinitions")
print("=" * 80)

db = SessionLocal()

try:
    # 1. 获取所有DELIVERY的FieldPipeline
    print("\n【Field Pipelines】")
    print("-" * 80)
    pipelines = db.query(FieldPipeline).filter(
        FieldPipeline.file_type == 'DELIVERY',
        FieldPipeline.enabled == True
    ).order_by(FieldPipeline.order_num).all()
    
    print(f"DELIVERY类型的FieldPipeline数量: {len(pipelines)}")
    
    # 收集所有引用的rule_ref
    referenced_rules = set()
    missing_rules = set()
    
    for p in pipelines:
        print(f"\n列 {p.target_col}: {p.target_header}")
        print(f"  map_op: {p.map_op}")
        print(f"  rule_ref: {p.rule_ref}")
        
        if p.rule_ref and isinstance(p.rule_ref, list) and len(p.rule_ref) > 0:
            for rule_ref in p.rule_ref:
                referenced_rules.add(rule_ref)
                print(f"    - 引用规则: {rule_ref}")
                
                # 检查规则是否存在
                rule = db.query(RuleDefinition).filter(
                    RuleDefinition.rule_ref == rule_ref,
                    RuleDefinition.enabled == True
                ).first()
                
                if rule:
                    print(f"      ✓ 规则存在 (类型: {rule.rule_type})")
                else:
                    print(f"      ✗ 规则不存在")
                    missing_rules.add(rule_ref)
        else:
            print(f"    无规则引用")
    
    # 2. 检查所有引用的规则是否存在
    print("\n" + "=" * 80)
    print("【规则引用汇总】")
    print("-" * 80)
    print(f"引用的规则总数: {len(referenced_rules)}")
    print(f"缺失的规则数: {len(missing_rules)}")
    
    if referenced_rules:
        print("\n所有引用的规则:")
        for rule_ref in sorted(referenced_rules):
            status = "✓" if rule_ref not in missing_rules else "✗"
            print(f"  {status} {rule_ref}")
    
    # 3. 检查RuleDefinitions表中的所有规则
    print("\n" + "=" * 80)
    print("【数据库中的所有RuleDefinitions】")
    print("-" * 80)
    all_rules = db.query(RuleDefinition).filter(
        RuleDefinition.enabled == True
    ).all()
    
    print(f"启用的RuleDefinition总数: {len(all_rules)}")
    
    for rule in all_rules:
        print(f"\nrule_ref: {rule.rule_ref}")
        print(f"  rule_type: {rule.rule_type}")
        print(f"  executor_type: {rule.executor_type}")
        print(f"  enabled: {rule.enabled}")
        if rule.schema_json:
            schema_str = str(rule.schema_json)[:100] if len(str(rule.schema_json)) > 100 else str(rule.schema_json)
            print(f"  schema_json: {schema_str}...")
    
    # 4. 检查是否有DELIVERY相关的规则
    print("\n" + "=" * 80)
    print("【DELIVERY相关规则】")
    print("-" * 80)
    # 通过描述或配置判断哪些规则可能用于DELIVERY
    delivery_related_rules = []
    for rule in all_rules:
        desc = rule.schema_json.get('desc', '') if rule.schema_json else ''
        if 'delivery' in desc.lower() or '配達' in desc or '時間帯' in desc or 'お届け' in desc:
            delivery_related_rules.append(rule)
    
    print(f"DELIVERY相关规则数: {len(delivery_related_rules)}")
    for rule in delivery_related_rules:
        print(f"  - {rule.rule_ref}")
        if rule.schema_json and 'desc' in rule.schema_json:
            print(f"    描述: {rule.schema_json['desc']}")
    
    # 5. 总结
    print("\n" + "=" * 80)
    print("【总结】")
    print("-" * 80)
    if missing_rules:
        print(f"[警告] 发现 {len(missing_rules)} 个缺失的规则:")
        for rule_ref in sorted(missing_rules):
            print(f"    - {rule_ref}")
        print("\n建议: 检查这些规则是否需要创建，或者从FieldPipeline中移除引用")
    else:
        print("[OK] 所有引用的规则都存在")
    
    if referenced_rules:
        print(f"\n[OK] DELIVERY的FieldPipelines引用了 {len(referenced_rules)} 个规则")
    else:
        print("[INFO] DELIVERY的FieldPipelines没有引用任何规则")
        print("  当前所有列都使用简单的COPY或CONST操作，无需额外规则处理")
    
    print("=" * 80)
    
except Exception as e:
    print(f"错误: {str(e)}")
    import traceback
    traceback.print_exc()
finally:
    db.close()
