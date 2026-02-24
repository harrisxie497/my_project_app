"""
检查所有AI列的提示词配置（详细版，保存到文件）
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.core.database import SessionLocal
from app.models.field_pipeline import FieldPipeline
from app.models.rule_definition import RuleDefinition
import json

def check_ai_columns_prompt_detailed_to_file():
    """检查所有AI列的提示词配置（详细版，保存到文件）"""
    output_file = os.path.join(os.path.dirname(__file__), 'ai_columns_prompt_check.txt')
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("=" * 100 + "\n")
        f.write("检查所有AI列的提示词配置（详细版）\n")
        f.write("=" * 100 + "\n\n")
        
        db_session = SessionLocal()
        
        try:
            # 查询所有AI类型的列
            ai_columns = db_session.query(FieldPipeline).filter(
                FieldPipeline.field_type == 'AI'
            ).order_by(FieldPipeline.target_col).all()
            
            f.write(f"找到 {len(ai_columns)} 个AI类型的列\n\n")
            
            for idx, column in enumerate(ai_columns, 1):
                f.write("=" * 100 + "\n")
                f.write(f"第 {idx} 个AI列\n")
                f.write("=" * 100 + "\n")
                f.write(f"列名: {column.target_col}\n")
                f.write(f"文件类型: {column.file_type}\n")
                f.write(f"操作类型: {column.map_op}\n")
                f.write(f"规则引用: {column.rule_ref}\n")
                f.write(f"源列: {column.source_cols}\n")
                
                # 显示field_pipelines表中的rule_params_json
                f.write("\n" + "-" * 100 + "\n")
                f.write("field_pipelines表中的rule_params_json:\n")
                f.write("-" * 100 + "\n")
                rule_params_json = column.rule_params_json
                if isinstance(rule_params_json, str):
                    rule_params_json = json.loads(rule_params_json)
                f.write(json.dumps(rule_params_json, indent=2, ensure_ascii=False) + "\n")
                
                # 查询对应的规则定义
                rule_ref = column.rule_ref[0] if isinstance(column.rule_ref, list) else column.rule_ref
                rule = db_session.query(RuleDefinition).filter(
                    RuleDefinition.rule_ref == rule_ref
                ).first()
                
                if rule:
                    # 显示rule_definitions表中的schema_json
                    f.write("\n" + "-" * 100 + "\n")
                    f.write("rule_definitions表中的schema_json:\n")
                    f.write("-" * 100 + "\n")
                    schema_json = rule.schema_json
                    if isinstance(schema_json, str):
                        schema_json = json.loads(schema_json)
                    f.write(json.dumps(schema_json, indent=2, ensure_ascii=False) + "\n")
                    
                    # 检查是否有重复的提示词
                    f.write("\n" + "-" * 100 + "\n")
                    f.write("重复检查:\n")
                    f.write("-" * 100 + "\n")
                    
                    # 检查rule_params_json中是否有prompt
                    if isinstance(rule_params_json, dict):
                        for key, value in rule_params_json.items():
                            if 'prompt' in value:
                                f.write(f"  [警告] rule_params_json.{key} 中包含 prompt 配置，应该删除\n")
                                f.write(f"  prompt 内容:\n{value.get('prompt', '')}\n\n")
                    
                    # 检查schema_json中是否有system_prompt
                    if isinstance(schema_json, dict) and 'configurable_params' in schema_json:
                        if 'system_prompt' in schema_json['configurable_params']:
                            f.write(f"  [信息] 规则定义中包含 system_prompt\n")
                            f.write(f"  system_prompt 内容:\n{schema_json['configurable_params']['system_prompt']}\n\n")
                else:
                    f.write(f"\n  [错误] 未找到对应的规则定义: {rule_ref}\n")
                
                f.write("\n")
        
        finally:
            db_session.close()
        
        f.write("=" * 100 + "\n")
        f.write("检查完成\n")
        f.write("=" * 100 + "\n")
    
    print(f"结果已保存到: {output_file}")

if __name__ == "__main__":
    check_ai_columns_prompt_detailed_to_file()
