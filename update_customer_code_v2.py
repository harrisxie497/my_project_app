"""
修改佐川顧客コード（固定）列的配置值
"""
import sys
import os
import io
import json

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from app.core.database import SessionLocal
from app.models.field_pipeline import FieldPipeline

db = SessionLocal()

print("=" * 80)
print("查询佐川顧客コード（固定）列的当前配置")
print("=" * 80)

# 查询佐川顧客コード（固定）列
pipeline = db.query(FieldPipeline).filter(
    FieldPipeline.target_header == '佐川顧客コード（固定）',
    FieldPipeline.file_type == 'DELIVERY'
).first()

if pipeline:
    print(f"\n当前配置:")
    print(f"  target_col: {pipeline.target_col}")
    print(f"  target_header: {pipeline.target_header}")
    print(f"  map_op: {pipeline.map_op}")
    print(f"  rule_params_json: {pipeline.rule_params_json}")
    print(f"  type: {type(pipeline.rule_params_json)}")

    # 直接修改嵌套字典
    new_value = '148202040055'

    if isinstance(pipeline.rule_params_json, dict):
        if 'policy_const' in pipeline.rule_params_json:
            pipeline.rule_params_json['policy_const']['value'] = new_value
            print(f"\n✅ 已将固定值修改为: {new_value}")
        else:
            print(f"\n⚠️  rule_params_json结构不符合预期")
    else:
        print(f"\n⚠️  rule_params_json不是dict类型")

    db.commit()

    # 重新查询验证
    db.refresh(pipeline)
    print(f"\n修改后的配置:")
    print(f"  rule_params_json: {pipeline.rule_params_json}")
else:
    print("\n❌ 未找到佐川顧客コード（固定）列的配置")

db.close()
