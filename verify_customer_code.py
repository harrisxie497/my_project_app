"""
验证佐川顧客コード（固定）列的配置值
"""
import sys
import os
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from app.core.database import SessionLocal
from app.models.field_pipeline import FieldPipeline

db = SessionLocal()

print("=" * 80)
print("验证佐川顧客コード（固定）列的配置")
print("=" * 80)

# 查询佐川顧客コード（固定）列
pipeline = db.query(FieldPipeline).filter(
    FieldPipeline.target_header == '佐川顧客コード（固定）',
    FieldPipeline.file_type == 'DELIVERY'
).first()

if pipeline:
    print(f"\n当前数据库中的配置:")
    print(f"  target_col: {pipeline.target_col}")
    print(f"  target_header: {pipeline.target_header}")
    print(f"  map_op: {pipeline.map_op}")
    print(f"  rule_params_json: {pipeline.rule_params_json}")

    # 检查值
    if isinstance(pipeline.rule_params_json, dict):
        if 'policy_const' in pipeline.rule_params_json:
            current_value = pipeline.rule_params_json['policy_const'].get('value', '')
            print(f"\n  当前固定值: {current_value}")
            if current_value == '148202040055':
                print(f"  ✅ 固定值正确！")
            else:
                print(f"  ❌ 固定值不正确，应该是 148202040055")

    # 直接更新
    new_value = '148202040055'
    if isinstance(pipeline.rule_params_json, dict):
        if 'policy_const' in pipeline.rule_params_json:
            pipeline.rule_params_json['policy_const']['value'] = new_value
            print(f"\n正在更新为: {new_value}")
            db.commit()
            print("✅ 更新成功！")
else:
    print("\n❌ 未找到佐川顧客コード（固定）列的配置")

db.close()
