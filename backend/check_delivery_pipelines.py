"""查看DELIVERY类型的field_pipeline配置"""
from app.core.database import SessionLocal
from app.models.field_pipeline import FieldPipeline
from app.models.file_definition import FileDefinition

db = SessionLocal()

# 查询DELIVERY类型的file_definition
file_defs = db.query(FileDefinition).filter(FileDefinition.file_type == 'DELIVERY').all()
print("DELIVERY文件定义:")
for fd in file_defs:
    print(f"  file_type: {fd.file_type}")
    print(f"  file_name: {fd.file_name}")
    print(f"  description: {fd.description}")
    print()

# 查询DELIVERY类型的field_pipeline
pipelines = db.query(FieldPipeline).filter(FieldPipeline.file_type == 'DELIVERY').order_by(FieldPipeline.order_num).all()
print(f"\nDELIVERY field_pipeline配置 (共{len(pipelines)}个):")
for p in pipelines:
    print(f"\nPipeline ID: {p.id}")
    print(f"  target_col: {p.target_col}")
    print(f"  target_header: {p.target_header}")
    print(f"  rule_ref: {p.rule_ref}")
    print(f"  source_cols: {p.source_cols}")
    print(f"  map_op: {p.map_op}")
    print(f"  depends_on: {p.depends_on}")
    print(f"  order_num: {p.order_num}")
    print(f"  enabled: {p.enabled}")

db.close()
