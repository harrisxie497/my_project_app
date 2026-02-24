"""
检查C列和D列的处理顺序
"""
from app.core.database import SessionLocal
from app.models.field_pipeline import FieldPipeline

print("=" * 80)
print("检查C列和D列的处理顺序")
print("=" * 80)

db = SessionLocal()

try:
    pipelines = db.query(FieldPipeline).filter(
        FieldPipeline.file_type == 'DELIVERY',
        FieldPipeline.target_col.in_(['C', 'D']),
        FieldPipeline.enabled == True
    ).order_by(FieldPipeline.order_num).all()

    print("\nC列和D列的配置:")
    for p in pipelines:
        print(f"\n列 {p.target_col} ({p.target_header}):")
        print(f"  order_num: {p.order_num}")
        print(f"  map_op: {p.map_op}")
        print(f"  source_cols: {p.source_cols}")
        print(f"  depends_on: {p.depends_on}")

except Exception as e:
    print(f"错误: {str(e)}")
finally:
    db.close()
