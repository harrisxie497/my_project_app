"""
删除所有AI列的field_pipelines.rule_params_json中的prompt配置
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.core.database import SessionLocal
from app.models.field_pipeline import FieldPipeline
import json

def remove_prompt_from_ai_columns():
    """删除所有AI列的field_pipelines.rule_params_json中的prompt配置"""
    print("=" * 100)
    print("删除所有AI列的field_pipelines.rule_params_json中的prompt配置")
    print("=" * 100)
    
    db_session = SessionLocal()
    
    try:
        # 查询所有AI类型的列
        ai_columns = db_session.query(FieldPipeline).filter(
            FieldPipeline.field_type == 'AI'
        ).order_by(FieldPipeline.target_col).all()
        
        print(f"\n找到 {len(ai_columns)} 个AI类型的列\n")
        
        for idx, column in enumerate(ai_columns, 1):
            print("=" * 100)
            print(f"处理第 {idx} 个AI列: {column.target_col}")
            print("=" * 100)
            
            # 显示修改前的配置
            rule_params_json = column.rule_params_json
            if isinstance(rule_params_json, str):
                rule_params_json = json.loads(rule_params_json)
            
            print(f"\n修改前:")
            print(f"  列名: {column.target_col}")
            print(f"  文件类型: {column.file_type}")
            print(f"  规则引用: {column.rule_ref}")
            print(f"  rule_params_json: {json.dumps(rule_params_json, indent=2, ensure_ascii=False)}")
            
            # 删除prompt配置
            if isinstance(rule_params_json, dict):
                for key, value in rule_params_json.items():
                    if 'prompt' in value:
                        print(f"\n  删除 rule_params_json.{key}.prompt 配置")
                        del value['prompt']
            
            # 更新配置
            column.rule_params_json = json.dumps(rule_params_json, ensure_ascii=False)
            
            print(f"\n修改后:")
            print(f"  rule_params_json: {json.dumps(rule_params_json, indent=2, ensure_ascii=False)}")
            print(f"\n  [成功] 已删除prompt配置")
            
            db_session.commit()
        
        print("\n" + "=" * 100)
        print(f"所有 {len(ai_columns)} 个AI列的prompt配置已删除")
        print("=" * 100)
    
    except Exception as e:
        db_session.rollback()
        print(f"\n[错误] 处理失败: {str(e)}")
        import traceback
        traceback.print_exc()
    
    finally:
        db_session.close()
    
    print("\n" + "=" * 100)
    print("处理完成")
    print("=" * 100)

if __name__ == "__main__":
    remove_prompt_from_ai_columns()
