"""
测试依頼主、依頼主住所、依頼主電話列是否正确使用默认值
"""
from app.core.database import SessionLocal
from app.models.field_pipeline import FieldPipeline
import json

print("=" * 80)
print("测试依頼主、依頼主住所、依頼主電話列的默认值配置")
print("=" * 80)

db = SessionLocal()

try:
    # 获取J、K、M三列的配置
    target_columns = {
        'J': {'header': '依頼主', 'expected_value': 'DIDA'},
        'K': {'header': '依頼主住所', 'expected_value': '千葉県流山市平方8061GLPALFALINK81F13番シャッター'},
        'M': {'header': '依頼主電話', 'expected_value': '0471377848'}
    }
    
    all_correct = True
    
    for col, config in target_columns.items():
        print(f"\n{'=' * 80}")
        print(f"列 {col} ({config['header']}):")
        print("-" * 80)
        
        pipeline = db.query(FieldPipeline).filter(
            FieldPipeline.file_type == 'DELIVERY',
            FieldPipeline.target_col == col,
            FieldPipeline.enabled == True
        ).first()
        
        if pipeline:
            print(f"  map_op: {pipeline.map_op}")
            print(f"  source_cols: {pipeline.source_cols}")
            print(f"  field_type: {pipeline.field_type}")
            print(f"  rule_params_json: {pipeline.rule_params_json}")
            
            # 检查配置是否正确
            is_correct = True
            
            if pipeline.map_op != 'DEFAULT':
                print(f"  [错误] map_op应该是DEFAULT，实际是{pipeline.map_op}")
                is_correct = False
            
            if pipeline.source_cols != [config['header']]:
                print(f"  [错误] source_cols应该是['{config['header']}']，实际是{pipeline.source_cols}")
                is_correct = False
            
            if not pipeline.rule_params_json:
                print(f"  [错误] rule_params_json为空")
                is_correct = False
            else:
                actual_value = pipeline.rule_params_json
                if actual_value != config['expected_value']:
                    print(f"  [错误] 默认值不匹配")
                    print(f"         期望: {config['expected_value']}")
                    print(f"         实际: {actual_value}")
                    is_correct = False
                else:
                    print(f"  [正确] 默认值匹配: {actual_value}")
            
            if is_correct:
                print(f"  [通过] 列配置正确：源值为空时使用默认值 '{config['expected_value']}'")
            else:
                print(f"  [失败] 列配置有误")
                all_correct = False
        else:
            print(f"  [错误] 未找到配置")
            all_correct = False
    
    print("\n" + "=" * 80)
    if all_correct:
        print("[成功] 所有列配置正确，将使用正确的默认值")
    else:
        print("[失败] 部分列配置有误，请检查")
    print("=" * 80)
    
except Exception as e:
    print(f"错误: {str(e)}")
    import traceback
    traceback.print_exc()
finally:
    db.close()
