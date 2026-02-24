"""
调试DEFAULT操作：查看实际的源值和规则参数
"""
from app.core.database import SessionLocal
from app.models.field_pipeline import FieldPipeline
from app.services.field_handlers import copy_equal_to

print("=" * 80)
print("调试DEFAULT操作")
print("=" * 80)

db = SessionLocal()

try:
    # 获取J列的配置
    pipeline = db.query(FieldPipeline).filter(
        FieldPipeline.file_type == 'DELIVERY',
        FieldPipeline.target_col == 'J',
        FieldPipeline.enabled == True
    ).first()

    if pipeline:
        print(f"\nJ列配置:")
        print(f"  target_header: {pipeline.target_header}")
        print(f"  map_op: {pipeline.map_op}")
        print(f"  source_cols: {pipeline.source_cols}")
        print(f"  rule_params_json: {pipeline.rule_params_json}")
        print(f"  rule_params_json类型: {type(pipeline.rule_params_json)}")

        # 测试不同的源值
        test_cases = [
            {"source_value": "TEST", "description": "有值的源值"},
            {"source_value": "", "description": "空字符串"},
            {"source_value": None, "description": "None值"}
        ]

        print(f"\n测试DEFAULT操作:")
        print("-" * 80)

        for test_case in test_cases:
            source_value = test_case["source_value"]
            description = test_case["description"]

            # 模拟delivery_processor的逻辑
            rule_params_json = pipeline.rule_params_json
            map_op = pipeline.map_op

            if map_op == 'DEFAULT':
                rule_params = rule_params_json
            else:
                rule_params = {}

            print(f"\n测试: {description}")
            print(f"  source_value: {repr(source_value)}")
            print(f"  rule_params (默认值): {repr(rule_params)}")
            print(f"  rule_params类型: {type(rule_params)}")

            result = copy_equal_to(source_value, rule_params)
            print(f"  结果: {repr(result)}")

            # 期望结果
            if source_value and (not isinstance(source_value, str) or source_value.strip() != ''):
                expected = source_value
            else:
                expected = rule_params

            if result == expected:
                print(f"  [通过]")
            else:
                print(f"  [失败] 期望: {repr(expected)}")
finally:
    db.close()
