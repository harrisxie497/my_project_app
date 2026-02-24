"""查看所有file_type和file_definition"""
from app.core.database import SessionLocal
from app.models.field_pipeline import FieldPipeline
from app.models.file_definition import FileDefinition

db = SessionLocal()

# 查询所有file_type
print('所有file_type:')
file_types = db.query(FieldPipeline.file_type).distinct().all()
print([ft[0] for ft in file_types])

# 查询所有file_definition
print('\n所有file_definition:')
file_defs = db.query(FileDefinition).all()
for fd in file_defs:
    print(f"  file_type: {fd.file_type}, file_name: {fd.file_name}, file_role: {fd.file_role}")

# 查询CUSTOMS的pipeline配置
print('\nCUSTOMS field_pipeline:')
customs_pipelines = db.query(FieldPipeline).filter(FieldPipeline.file_type == 'CUSTOMS').order_by(FieldPipeline.order_num).all()
print(f"共{len(customs_pipelines)}个:")
for p in customs_pipelines:
    print(f"  {p.target_col} -> {p.target_header}, rule_ref: {p.rule_ref}")

db.close()
