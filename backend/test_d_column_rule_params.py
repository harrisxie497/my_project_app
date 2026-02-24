"""
查看D列的rule_params_json配置
"""

from app.services.excel_reader import read_excel_file
from app.services.customs_processor import CustomsProcessor
from app.core.database import SessionLocal
import logging
import json

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def test_d_column_rule_params():
    """查看D列的rule_params_json配置"""
    print("=" * 100)
    print("查看D列的rule_params_json配置")
    print("=" * 100)
    
    task_dir = "C:\\Users\\harris.xie\\Documents\\trae_projects\\japan\\backend\\storage\\tasks\\t_2174140b"
    
    db_session = SessionLocal()
    try:
        processor = CustomsProcessor(
            task_dir=task_dir,
            db_session=db_session,
            file_type='CUSTOMS'
        )
        
        # 获取D列的配置
        field_pipelines = processor._get_field_pipelines()
        d_pipeline = next((p for p in field_pipelines if p.get('target_col') == 'D'), None)
        
        if d_pipeline:
            print(f"\nD列的配置:")
            print(f"  map_op: {d_pipeline.get('map_op')}")
            print(f"  source_cols: {d_pipeline.get('source_cols')}")
            print(f"  field_type: {d_pipeline.get('field_type')}")
            print(f"  rule_ref: {d_pipeline.get('rule_ref')}")
            print(f"  depends_on: {d_pipeline.get('depends_on')}")
            print(f"  rule_params_json:")
            rule_params_json = d_pipeline.get('rule_params_json', {})
            print(f"    {json.dumps(rule_params_json, ensure_ascii=False, indent=6)}")
        
    except Exception as e:
        print(f"\n测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        db_session.close()


if __name__ == "__main__":
    test_d_column_rule_params()
