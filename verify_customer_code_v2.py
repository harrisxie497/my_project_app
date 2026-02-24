"""
重新验证并修改佐川顧客コード（固定）列的配置值
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
print("修改佐川顧客コード（固定）列的配置")
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

    # 检查当前值
    if isinstance(pipeline.rule_params_json, dict):
        if 'policy_const' in pipeline.rule_params_json:
            current_value = pipeline.rule_params_json['policy_const'].get('value', '')
            print(f"\n  当前固定值: {current_value}")

            # 直接修改
            new_value = '148202040055'
            pipeline.rule_params_json['policy_const']['value'] = new_value
            print(f"  正在更新为: {new_value}")

            # 提交到数据库
            db.commit()
            print("  ✅ 已提交到数据库")

            # 重新查询验证
            db.expire_all()  # 清除session缓存
            pipeline2 = db.query(FieldPipeline).filter(
                FieldPipeline.target_header == '佐川顧客コード（固定）',
                FieldPipeline.file_type == 'DELIVERY'
            ).first()

            if pipeline2:
                updated_value = pipeline2.rule_params_json['policy_const'].get('value', '')
                print(f"\n  数据库中的值: {updated_value}")
                if updated_value == new_value:
                    print(f"  ✅ 更新成功！")
                else:
                    print(f"  ❌ 更新失败！")
else:
    print("\n❌ 未找到佐川顧客コード（固定）列的配置")

db.close()
