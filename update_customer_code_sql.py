"""
使用SQL直接更新佐川顧客コード（固定）列的配置值
"""
import sys
import os
import io
import json

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from app.core.database import SessionLocal
from sqlalchemy import text

db = SessionLocal()

print("=" * 80)
print("使用SQL直接更新佐川顧客コード（固定）列的配置")
print("=" * 80)

try:
    # 查询当前配置
    result = db.execute(text(
        "SELECT id, rule_params_json FROM field_pipelines "
        "WHERE target_header = '佐川顧客コード（固定）' AND file_type = 'DELIVERY'"
    )).fetchone()

    if result:
        pipeline_id = result[0]
        rule_params_json_str = result[1]

        print(f"\n当前配置:")
        print(f"  id: {pipeline_id}")
        print(f"  rule_params_json: {rule_params_json_str}")

        # 解析并修改
        if rule_params_json_str:
            rule_params = json.loads(rule_params_json_str) if isinstance(rule_params_json_str, str) else rule_params_json_str
            if 'policy_const' in rule_params:
                new_value = '148202040055'
                rule_params['policy_const']['value'] = new_value
                new_rule_params_json = json.dumps(rule_params, ensure_ascii=False)

                print(f"\n修改为: {new_value}")
                print(f"新的JSON: {new_rule_params_json}")

                # 执行更新
                update_sql = text(
                    "UPDATE field_pipelines SET rule_params_json = :rule_params_json "
                    "WHERE id = :id"
                )

                db.execute(update_sql, {"rule_params_json": new_rule_params_json, "id": pipeline_id})
                db.commit()

                print("\n✅ SQL更新成功！")

                # 验证更新
                verify_result = db.execute(text(
                    "SELECT rule_params_json FROM field_pipelines "
                    "WHERE id = :id"
                ), {"id": pipeline_id}).fetchone()

                if verify_result:
                    verify_json = json.loads(verify_result[0]) if verify_result[0] else None
                    if verify_json and 'policy_const' in verify_json:
                        verify_value = verify_json['policy_const'].get('value', '')
                        print(f"\n数据库验证 - 固定值: {verify_value}")
                        if verify_value == new_value:
                            print("✅ 验证成功！")
                        else:
                            print("❌ 验证失败！")
            else:
                print("\n❌ rule_params_json结构不符合预期")
        else:
            print("\n❌ rule_params_json为空")
    else:
        print("\n❌ 未找到配置")

except Exception as e:
    print(f"\n❌ 错误: {str(e)}")
    import traceback
    traceback.print_exc()
finally:
    db.close()
