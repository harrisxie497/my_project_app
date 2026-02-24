#!/usr/bin/env python3
"""
测试F列使用新规则 policy_copy_one_decimal 的处理效果
"""

import sys
import os
sys.path.insert(0, 'c:/Users/harris.xie/Documents/trae_projects/japan/backend')

from dotenv import load_dotenv
from app.core.database import SessionLocal
from app.models.field_pipeline import FieldPipeline
from app.models.rule_definition import RuleDefinition
from app.services.field_handlers_v2 import process_field_v2

load_dotenv(dotenv_path='c:/Users/harris.xie/Documents/trae_projects/japan/backend/.env')

# 初始化数据库
db = SessionLocal()

# 测试数据
test_data = [
    {
        '_row_index': 0,
        'F': '1.234',
        'H': '飞轮玩具(12-24M)',
        'I': 'ABS(100%)',
    },
    {
        '_row_index': 1,
        'F': '2.567',
        'H': 'T恤(L码)',
        'I': '棉(100%)',
    },
    {
        '_row_index': 2,
        'F': '0.890',
        'H': '连衣裙(XL码)',
        'I': '涤纶(100%)',
    },
    {
        '_row_index': 3,
        'F': '3.500',
        'H': '鞋子',
        'I': '皮革',
    },
    {
        '_row_index': 4,
        'F': '5.123kg',
        'H': '包包',
        'I': '帆布',
    },
    {
        '_row_index': 5,
        'F': '',
        'H': '帽子',
        'I': '棉',
    },
    {
        '_row_index': 6,
        'F': None,
        'H': '手套',
        'I': '羊毛',
    },
    {
        '_row_index': 7,
        'F': 'abc',
        'H': '袜子',
        'I': '棉',
    },
]

print("=" * 80)
print("测试F列使用新规则 policy_copy_one_decimal")
print("=" * 80)

# 获取F列的pipeline配置
pipelines = db.query(FieldPipeline).filter(
    FieldPipeline.target_col == 'F',
    FieldPipeline.file_type == 'CUSTOMS',
    FieldPipeline.enabled == True
).all()

if not pipelines:
    print("未找到F列的pipeline配置")
    db.close()
    sys.exit(1)

pipeline = pipelines[0]
print(f"\nPipeline配置：")
print(f"  target_col: {pipeline.target_col}")
print(f"  target_header: {pipeline.target_header}")
print(f"  rule_ref: {pipeline.rule_ref}")
print(f"  source_cols: {pipeline.source_cols}")

# 获取规则参数
rules = db.query(RuleDefinition).filter(
    RuleDefinition.rule_ref.in_(pipeline.rule_ref)
).all()

rule_params_json = {}
for rule in rules:
    if rule.rule_ref in pipeline.rule_ref:
        rule_params_json[rule.rule_ref] = rule.schema_json

print(f"\n规则参数：")
for rule_ref, params in rule_params_json.items():
    print(f"  {rule_ref}:")
    print(f"    handler: {params.get('handler')}")
    print(f"    desc: {params.get('desc')}")

# 构建完整的pipeline配置
full_pipeline = {
    'target_col': pipeline.target_col,
    'target_header': pipeline.target_header,
    'rule_ref': pipeline.rule_ref,
    'source_cols': pipeline.source_cols,
    'rule_params_json': rule_params_json,
}

print("\n" + "=" * 80)
print("处理测试数据")
print("=" * 80)

# 处理每条测试数据
for i, row_data in enumerate(test_data, 1):
    print(f"\n测试用例 {i}:")
    print(f"  输入: F={repr(row_data.get('F'))}")

    try:
        result = process_field_v2(
            map_op='COPY',
            source_cols=['F'],
            field_type='TEXT',
            rule_ref=pipeline.rule_ref,
            row=row_data,
            pipeline=full_pipeline,
        )

        print(f"  输出: {repr(result)}")

        # 验证结果
        expected = ""
        f_value = row_data.get('F')
        if f_value:
            # 去掉非数字字符
            import re
            cleaned = re.sub(r'[^\d.]', '', str(f_value))
            if cleaned:
                try:
                    float_val = float(cleaned)
                    expected = f"{round(float_val, 1):.1f}"
                except ValueError:
                    expected = ""

        print(f"  期望: {repr(expected)}")
        print(f"  状态: {'[通过]' if repr(result) == repr(expected) else '[失败]'}")

    except Exception as e:
        print(f"  异常: {e}")
        import traceback
        traceback.print_exc()

print("\n" + "=" * 80)
print("测试完成")
print("=" * 80)

db.close()
