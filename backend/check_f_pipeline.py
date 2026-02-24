#!/usr/bin/env python3
import sys
sys.path.insert(0, 'c:/Users/harris.xie/Documents/trae_projects/japan/backend')

from app.core.database import SessionLocal
from app.models.field_pipeline import FieldPipeline
import json

db = SessionLocal()

# 查找F列的pipeline配置
pipelines = db.query(FieldPipeline).filter(
    FieldPipeline.target_col == 'F',
    FieldPipeline.file_type == 'CUSTOMS'
).all()

print(f"F列的pipeline配置：\n")
for i, pipeline in enumerate(pipelines, 1):
    print(f"Pipeline {i}:")
    print(f"  target_col: {pipeline.target_col}")
    print(f"  target_header: {pipeline.target_header}")
    print(f"  rule_ref: {pipeline.rule_ref}")
    print(f"  source_cols: {pipeline.source_cols}")
    print(f"  enabled: {pipeline.enabled}")
    print()

db.close()
