"""
检查MySQL数据库中的DELIVERY配置
"""
from app.core.database import SessionLocal
from app.models.file_definition import FileDefinition
from app.models.field_pipeline import FieldPipeline

print("=" * 80)
print("检查MySQL数据库中的DELIVERY配置")
print("=" * 80)

db = SessionLocal()

try:
    # 检查File Definitions
    print("\n【File Definitions】")
    print("-" * 80)
    file_defs = db.query(FileDefinition).filter(
        FileDefinition.file_type == 'DELIVERY'
    ).all()
    
    print(f"DELIVERY类型的FileDefinition数量: {len(file_defs)}")
    
    for fd in file_defs:
        print(f"\nID: {fd.id}")
        print(f"  file_type: {fd.file_type}")
        print(f"  file_role: {fd.file_role}")
        print(f"  sheet_name: {fd.sheet_name}")
        print(f"  header_row: {fd.header_row}")
        print(f"  data_start_row: {fd.data_start_row}")
        print(f"  enabled: {fd.enabled}")
        print(f"  columns_json类型: {type(fd.columns_json)}")
        if isinstance(fd.columns_json, list):
            print(f"  列数量: {len(fd.columns_json)}")
            print(f"  列信息(前5个): {fd.columns_json[:5]}")
        else:
            print(f"  columns_json: {fd.columns_json}")
    
    # 检查Field Pipelines
    print("\n" + "=" * 80)
    print("【Field Pipelines】")
    print("-" * 80)
    pipelines = db.query(FieldPipeline).filter(
        FieldPipeline.file_type == 'DELIVERY'
    ).order_by(FieldPipeline.order_num).all()
    
    print(f"DELIVERY类型的FieldPipeline数量: {len(pipelines)}")
    
    for p in pipelines:
        print(f"\nID: {p.id}")
        print(f"  target_col: {p.target_col}")
        print(f"  target_header: {p.target_header}")
        print(f"  map_op: {p.map_op}")
        print(f"  source_cols: {p.source_cols}")
        print(f"  field_type: {p.field_type}")
        print(f"  rule_ref: {p.rule_ref}")
        print(f"  rule_params_json: {p.rule_params_json}")
        print(f"  depends_on: {p.depends_on}")
        print(f"  order_num: {p.order_num}")
        print(f"  enabled: {p.enabled}")
    
    print("\n" + "=" * 80)
    if len(file_defs) >= 2 and len(pipelines) >= 16:
        print("✅ DELIVERY配置完整，可以进行任务创建测试")
    else:
        print("⚠️  DELIVERY配置不完整")
        print(f"   FileDefinitions: 需要2个，当前{len(file_defs)}个")
        print(f"   FieldPipelines: 需要16-17个，当前{len(pipelines)}个")
    print("=" * 80)
    
except Exception as e:
    print(f"错误: {str(e)}")
    import traceback
    traceback.print_exc()
finally:
    db.close()
