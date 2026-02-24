"""
检查B列和L列的配置
"""

from app.services.excel_reader import read_excel_file
from app.services.customs_processor import CustomsProcessor
from app.core.database import SessionLocal
import logging
import json

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def test_b_l_columns_config():
    """检查B列和L列的配置"""
    print("=" * 100)
    print("检查B列和L列的配置")
    print("=" * 100)
    
    task_dir = "C:\\Users\\harris.xie\\Documents\\trae_projects\\japan\\backend\\storage\\tasks\\t_2174140b"
    
    db_session = SessionLocal()
    try:
        processor = CustomsProcessor(
            task_dir=task_dir,
            db_session=db_session,
            file_type='CUSTOMS'
        )
        
        # 获取field_pipelines配置
        field_pipelines = processor._get_field_pipelines()
        
        # 按order_num排序
        field_pipelines_sorted = sorted(field_pipelines, key=lambda x: x.get('order_num', 999))
        
        # 只处理B列和L列
        bl_pipelines = [p for p in field_pipelines_sorted if p.get('target_col') in ['B', 'L']]
        
        print(f"\nB列和L列的配置:")
        for pipeline in bl_pipelines:
            print(f"\n列 {pipeline.get('target_col')} ({pipeline.get('target_header')}):")
            print(f"  order_num: {pipeline.get('order_num')}")
            print(f"  map_op: {pipeline.get('map_op')}")
            print(f"  source_cols: {pipeline.get('source_cols')}")
            print(f"  field_type: {pipeline.get('field_type')}")
            print(f"  rule_ref: {pipeline.get('rule_ref')}")
            print(f"  depends_on: {pipeline.get('depends_on')}")
            print(f"  rule_params_json:")
            rule_params_json = pipeline.get('rule_params_json', {})
            print(f"    {json.dumps(rule_params_json, ensure_ascii=False, indent=6)}")
        
    except Exception as e:
        print(f"\n测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        db_session.close()


if __name__ == "__main__":
    test_b_l_columns_config()
