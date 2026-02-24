"""
检查所有AI列的提示词配置
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.core.database import SessionLocal
from app.models.field_pipeline import FieldPipeline
from app.models.rule_definition import RuleDefinition
import json

def check_ai_columns_prompt():
    """检查所有AI列的提示词配置"""
    print("=" * 100)
    print("检查所有AI列的提示词配置")
    print("=" * 100)
    
    db_session = SessionLocal()
    
    try:
        # 查询所有AI类型的列
        ai_columns = db_session.query(FieldPipeline).filter(
            FieldPipeline.field_type == 'AI'
        ).all()
        
        print(f"\n找到 {len(ai_columns)} 个AI类型的列")
        
        for column in ai_columns:
            print(f"\n{'=' * 100}")
            print(f"列名: {column.target_col}")
            print(f"文件类型: {column.file_type}")
            print(f"操作类型: {column.map_op}")
            print(f"规则引用: {column.rule_ref}")
            print(f"规则参数 (field_pipelines.rule_params_json): {column.rule_params_json}")
            
            # 查询对应的规则定义
            rule = db_session.query(RuleDefinition).filter(
                RuleDefinition.rule_ref == column.rule_ref[0] if isinstance(column.rule_ref, list) else column.rule_ref
            ).first()
            
            if rule:
                print(f"规则定义 (rule_definitions.schema_json): {rule.schema_json}")
                
                # 检查是否有重复的提示词
                rule_params_json = column.rule_params_json
                schema_json = rule.schema_json
                
                if isinstance(rule_params_json, str):
                    rule_params_json = json.loads(rule_params_json)
                if isinstance(schema_json, str):
                    schema_json = json.loads(schema_json)
                
                # 检查rule_params_json中是否有prompt
                if isinstance(rule_params_json, dict):
                    for key, value in rule_params_json.items():
                        if 'prompt' in value:
                            print(f"\n  警告: rule_params_json.{key} 中包含 prompt 配置，应该删除")
                            print(f"  prompt 内容: {value.get('prompt', '')}")
                
                # 检查schema_json中是否有system_prompt
                if isinstance(schema_json, dict) and 'configurable_params' in schema_json:
                    if 'system_prompt' in schema_json['configurable_params']:
                        print(f"\n  规则定义中包含 system_prompt")
                        print(f"  system_prompt 内容: {schema_json['configurable_params']['system_prompt'][:200]}...")
            else:
                print(f"\n  未找到对应的规则定义")
    
    finally:
        db_session.close()
    
    print("\n" + "=" * 100)
    print("检查完成")
    print("=" * 100)

if __name__ == "__main__":
    check_ai_columns_prompt()
