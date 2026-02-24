"""
更新依頼主、依頼主住所、依頼主電話三列为使用默认值
"""
from app.core.database import SessionLocal
from app.models.field_pipeline import FieldPipeline
import json

print("=" * 80)
print("更新依頼主、依頼主住所、依頼主電話列为使用默认值")
print("=" * 80)

db = SessionLocal()

try:
    # 定义要更新的列及其默认值
    columns_update = {
        'J': {
            'header': '依頼主',
            'default_value': 'DIDA'
        },
        'K': {
            'header': '依頼主住所',
            'default_value': '千葉県流山市平方8061GLPALFALINK81F13番シャッター'
        },
        'M': {
            'header': '依頼主電話',
            'default_value': '0471377848'
        }
    }
    
    for col, config in columns_update.items():
        print(f"\n{'=' * 80}")
        print(f"更新列 {col} ({config['header']}):")
        print("-" * 80)
        
        pipeline = db.query(FieldPipeline).filter(
            FieldPipeline.file_type == 'DELIVERY',
            FieldPipeline.target_col == col
        ).first()
        
        if pipeline:
            print(f"  旧配置:")
            print(f"    map_op: {pipeline.map_op}")
            print(f"    source_cols: {pipeline.source_cols}")
            print(f"    rule_params_json: {pipeline.rule_params_json}")
            
            # 更新配置为DEFAULT操作：源值为空时使用默认值
            pipeline.map_op = 'DEFAULT'
            pipeline.source_cols = [config['header']]  # 恢复源列
            # 设置rule_params_json为默认值（直接是值，不是policy_const结构）
            pipeline.rule_params_json = config['default_value']
            
            print(f"  新配置:")
            print(f"    map_op: {pipeline.map_op}")
            print(f"    source_cols: {pipeline.source_cols}")
            print(f"    default_value: {config['default_value']}")
            print(f"    rule_params_json: {pipeline.rule_params_json}")
            
            print(f"  已更新")
        else:
            print(f"  ✗ 未找到配置")
    
    # 提交更改
    db.commit()
    print("\n" + "=" * 80)
    print("所有更改已保存到数据库")
    print("=" * 80)
    
except Exception as e:
    db.rollback()
    print(f"错误: {str(e)}")
    import traceback
    traceback.print_exc()
finally:
    db.close()
