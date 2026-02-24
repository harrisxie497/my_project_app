#!/usr/bin/env python3
"""
创建新规则：policy_copy_one_decimal
更新F列的配置：从policy_ai_decimal_fix改为policy_copy_one_decimal
"""

import sys
import json
from sqlalchemy import create_engine, text

sys.path.insert(0, 'c:/Users/harris.xie/Documents/trae_projects/japan/backend')

from dotenv import load_dotenv
from app.core.database import SessionLocal
from app.models.rule_definition import RuleDefinition
from app.models.field_pipeline import FieldPipeline

load_dotenv(dotenv_path='c:/Users/harris.xie/Documents/trae_projects/japan/backend/.env')

def create_and_update():
    """创建新规则并更新F列配置"""
    db = SessionLocal()

    try:
        # ========================================
        # 步骤1：创建新规则 policy_copy_one_decimal
        # ========================================
        print("=" * 80)
        print("步骤1：创建新规则 policy_copy_one_decimal")
        print("=" * 80)

        # 检查规则是否已存在
        existing_rule = db.query(RuleDefinition).filter(
            RuleDefinition.rule_ref == 'policy_copy_one_decimal'
        ).first()

        if existing_rule:
            print(f"\n规则 'policy_copy_one_decimal' 已存在，将被更新")
        else:
            print(f"\n创建新规则 'policy_copy_one_decimal'")

        # 创建/更新规则
        new_rule = {
            "rule_ref": "policy_copy_one_decimal",
            "rule_type": "FORMAT",
            "executor_type": "program",
            "enabled": True,
            "schema_json": {
                "desc": "复制源值：保留1位小数，去掉非数字和小数点的字符",
                "handler": "normalize.copy_one_decimal",
                "configurable_params": {
                    "allow_null": True
                }
            }
        }

        if existing_rule:
            # 更新现有规则
            existing_rule.rule_type = new_rule["rule_type"]
            existing_rule.executor_type = new_rule["executor_type"]
            existing_rule.schema_json = new_rule["schema_json"]
        else:
            # 创建新规则
            existing_rule = RuleDefinition(**new_rule)
            db.add(existing_rule)

        print(f"\n规则配置：")
        print(json.dumps(new_rule["schema_json"], indent=2, ensure_ascii=False))

        # ========================================
        # 步骤2：更新F列的field_pipeline配置
        # ========================================
        print("\n" + "=" * 80)
        print("步骤2：更新F列的field_pipeline配置")
        print("=" * 80)

        # 查找所有F列的pipeline配置
        pipelines = db.query(FieldPipeline).filter(
            FieldPipeline.target_col == 'F',
            FieldPipeline.file_type == 'CUSTOMS'
        ).all()

        print(f"\n找到 {len(pipelines)} 个F列的pipeline配置")

        for i, pipeline in enumerate(pipelines, 1):
            print(f"\nPipeline {i}:")
            print(f"  旧规则: {pipeline.rule_ref}")
            print(f"  target_header: {pipeline.target_header}")

            # 更新规则引用
            pipeline.rule_ref = ['policy_copy_one_decimal']

            print(f"  新规则: {pipeline.rule_ref}")
            print(f"  [已更新]")

        # 提交所有更改
        db.commit()

        print("\n" + "=" * 80)
        print("✅ 配置更新成功！")
        print("=" * 80)

        # ========================================
        # 步骤3：验证更新结果
        # ========================================
        print("\n" + "=" * 80)
        print("步骤3：验证更新结果")
        print("=" * 80)

        # 验证规则
        rule = db.query(RuleDefinition).filter(
            RuleDefinition.rule_ref == 'policy_copy_one_decimal'
        ).first()

        if rule:
            print(f"\n✅ 规则验证成功：")
            print(f"  rule_ref: {rule.rule_ref}")
            print(f"  rule_type: {rule.rule_type}")
            print(f"  executor_type: {rule.executor_type}")
            print(f"  enabled: {rule.enabled}")
            print(f"  desc: {rule.schema_json.get('desc')}")
            print(f"  handler: {rule.schema_json.get('handler')}")
        else:
            print(f"\n❌ 规则验证失败：未找到 policy_copy_one_decimal")

        # 验证pipeline
        pipelines = db.query(FieldPipeline).filter(
            FieldPipeline.target_col == 'F',
            FieldPipeline.file_type == 'CUSTOMS'
        ).all()

        print(f"\n✅ Pipeline验证成功（{len(pipelines)}个配置）：")
        for i, pipeline in enumerate(pipelines, 1):
            print(f"  {i}. rule_ref: {pipeline.rule_ref}, target_header: {pipeline.target_header}")

    except Exception as e:
        db.rollback()
        print(f"\n❌ 配置更新失败: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    create_and_update()
