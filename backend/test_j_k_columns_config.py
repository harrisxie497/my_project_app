"""
检查J列和K列的配置
"""

from app.services.customs_processor import CustomsProcessor
from app.core.database import SessionLocal
import logging
import json

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def test_j_k_columns_config():
    """检查J列和K列的配置"""
    print("=" * 100)
    print("检查J列和K列的配置")
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
        
        # 只处理J列和K列
        for pipeline in field_pipelines_sorted:
            target_col = pipeline.get('target_col')
            if target_col in ['J', 'K']:
                print(f"\n列 {target_col}的配置:")
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
    test_j_k_columns_config()
