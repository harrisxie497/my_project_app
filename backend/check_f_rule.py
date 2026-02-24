#!/usr/bin/env python3
import sys
sys.path.insert(0, 'c:/Users/harris.xie/Documents/trae_projects/japan/backend')

from app.core.database import SessionLocal
from app.models.field_pipeline import FieldPipeline

db = SessionLocal()
pipelines = db.query(FieldPipeline).filter(
    FieldPipeline.target_col == 'F',
    FieldPipeline.file_type == 'CUSTOMS'
).all()
print('F column config:')
for p in pipelines:
    print(f'  target_col: {p.target_col}, rule_ref: {p.rule_ref}')
db.close()
