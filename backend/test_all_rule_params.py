"""
测试查看所有列的rule_params_json配置
"""

from app.services.customs_processor import CustomsProcessor
from app.core.database import SessionLocal
import logging
import json

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def test_all_rule_params():
    """测试查看所有列的rule_params_json配置"""
    print("=" * 100)
    print("测试查看所有列的rule_params_json配置")
    print("=" * 100)
    
    task_dir = "C:\\Users\\harris.xie\\Documents\\trae_projects\\japan\\backend\\storage\\tasks\\t_2174140b"
    
    db_session = SessionLocal()
    try:
        processor = CustomsProcessor(
            task_dir=task_dir,
            db_session=db_session,
            file_type='CUSTOMS'
        )
        
        field_pipelines = processor._get_field_pipelines()
        
        print(f"\n获取到 {len(field_pipelines)} 个字段处理配置\n")
        
        for pipeline in field_pipelines:
            target_col = pipeline.get('target_col')
            target_header = pipeline.get('target_header')
            map_op = pipeline.get('map_op')
            source_cols = pipeline.get('source_cols')
            field_type = pipeline.get('field_type')
            rule_ref = pipeline.get('rule_ref')
            depends_on = pipeline.get('depends_on')
            rule_params_json = pipeline.get('rule_params_json')
            
            print(f"列 {target_col} ({target_header}):")
            print(f"  map_op: {map_op}")
            print(f"  source_cols: {source_cols}")
            print(f"  field_type: {field_type}")
            print(f"  rule_ref: {rule_ref}")
            print(f"  depends_on: {depends_on}")
            if rule_params_json:
                print(f"  rule_params_json:")
                for rule_name, params in rule_params_json.items():
                    print(f"    {rule_name}:")
                    print(f"      输入: source_cols={source_cols}, depends_on={depends_on}")
                    print(f"      参数: {json.dumps(params, ensure_ascii=False, indent=6)}")
            else:
                print(f"  rule_params_json: None")
            print()
        
    except Exception as e:
        print(f"\n测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        db_session.close()


if __name__ == "__main__":
    test_all_rule_params()
