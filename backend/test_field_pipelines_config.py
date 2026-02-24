"""
测试查看field_pipelines配置
"""

from app.services.customs_processor import CustomsProcessor
from app.core.database import SessionLocal
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def test_field_pipelines_config():
    """测试查看field_pipelines配置"""
    print("=" * 100)
    print("测试查看field_pipelines配置")
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
        
        print(f"\n获取到 {len(field_pipelines)} 个字段处理配置")
        
        # 只显示A、B、C、D列的配置
        abcd_pipelines = [p for p in field_pipelines if p.get('target_col') in ['A', 'B', 'C', 'D']]
        
        print(f"\nA、B、C、D列的配置:")
        for pipeline in abcd_pipelines:
            print(f"\n列 {pipeline.get('target_col')}:")
            print(f"  target_col: {pipeline.get('target_col')}")
            print(f"  target_header: {pipeline.get('target_header')}")
            print(f"  map_op: {pipeline.get('map_op')}")
            print(f"  source_cols: {pipeline.get('source_cols')}")
            print(f"  field_type: {pipeline.get('field_type')}")
            print(f"  rule_ref: {pipeline.get('rule_ref')}")
            print(f"  depends_on: {pipeline.get('depends_on')}")
            print(f"  order: {pipeline.get('order')}")
            print(f"  const_value: {pipeline.get('const_value')}")
            print(f"  完整配置: {pipeline}")
        
    except Exception as e:
        print(f"\n测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        db_session.close()


if __name__ == "__main__":
    test_field_pipelines_config()
