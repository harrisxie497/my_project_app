"""
检查field_pipelines的order_num与file_definitions的columns_json顺序是否一致
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.core.database import SessionLocal
from app.models.field_pipeline import FieldPipeline
from app.models.file_definition import FileDefinition

def check_order_consistency():
    """检查顺序一致性"""
    print("=" * 100)
    print("检查field_pipelines的order_num与file_definitions的columns_json顺序一致性")
    print("=" * 100)
    
    db_session = SessionLocal()
    
    try:
        # 查询file_definitions中OUTPUT的columns_json
        output_file_def = db_session.query(FileDefinition).filter(
            FileDefinition.file_type == 'CUSTOMS',
            FileDefinition.file_role == 'OUTPUT'
        ).first()
        
        if not output_file_def:
            print("未找到OUTPUT文件定义")
            return
        
        output_columns = output_file_def.columns_json
        print(f"\nOUTPUT文件定义的列顺序（共{len(output_columns)}列）:")
        for idx, col in enumerate(output_columns, start=1):
            print(f"  {idx}. 列字母: {col.get('col')}, 表头: {col.get('header')}")
        
        # 查询field_pipelines
        field_pipelines = db_session.query(FieldPipeline).filter(
            FieldPipeline.file_type == 'CUSTOMS',
            FieldPipeline.enabled == True
        ).order_by(FieldPipeline.order_num).all()
        
        print(f"\n\nfield_pipelines的列顺序（共{len(field_pipelines)}列）:")
        for idx, pipeline in enumerate(field_pipelines, start=1):
            print(f"  {idx}. order_num: {pipeline.order_num}, 列字母: {pipeline.target_col}, 表头: {pipeline.target_header}")
        
        # 检查顺序是否一致
        print(f"\n\n顺序一致性检查:")
        output_headers = [col.get('header') for col in output_columns]
        pipeline_headers = [pipeline.target_header for pipeline in field_pipelines]
        
        if output_headers == pipeline_headers:
            print("  ✓ 顺序完全一致")
        else:
            print("  ✗ 顺序不一致")
            print(f"\n  OUTPUT定义的表头: {output_headers}")
            print(f"  field_pipelines的表头: {pipeline_headers}")
            
            # 找出不一致的地方
            print(f"\n  不一致的列:")
            for idx, (output_header, pipeline_header) in enumerate(zip(output_headers, pipeline_headers), start=1):
                if output_header != pipeline_header:
                    print(f"    第{idx}列: OUTPUT定义='{output_header}', field_pipelines='{pipeline_header}'")
        
        # 检查field_pipelines中的列是否都在OUTPUT定义中
        print(f"\n\nfield_pipelines中的列是否都在OUTPUT定义中:")
        for pipeline in field_pipelines:
            found = False
            for col in output_columns:
                if col.get('header') == pipeline.target_header:
                    found = True
                    break
            if found:
                print(f"  ✓ {pipeline.target_col} ({pipeline.target_header})")
            else:
                print(f"  ✗ {pipeline.target_col} ({pipeline.target_header}) - 未在OUTPUT定义中找到")
        
        # 检查OUTPUT定义中的列是否都在field_pipelines中
        print(f"\n\nOUTPUT定义中的列是否都在field_pipelines中:")
        for col in output_columns:
            found = False
            for pipeline in field_pipelines:
                if pipeline.target_header == col.get('header'):
                    found = True
                    break
            if found:
                print(f"  ✓ {col.get('col')} ({col.get('header')})")
            else:
                print(f"  ✗ {col.get('col')} ({col.get('header')}) - 未在field_pipelines中找到")
    
    except Exception as e:
        print(f"检查失败: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        db_session.close()
    
    print("\n" + "=" * 100)
    print("检查完成")
    print("=" * 100)

if __name__ == "__main__":
    check_order_consistency()
