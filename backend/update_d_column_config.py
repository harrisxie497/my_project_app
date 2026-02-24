"""
更新D列的配置，添加对C列的依赖
"""
from app.core.database import SessionLocal
from app.models.field_pipeline import FieldPipeline
import json

print("=" * 80)
print("更新D列（時間帯指定）的配置")
print("=" * 80)

db = SessionLocal()

try:
    # 获取D列的配置
    pipeline = db.query(FieldPipeline).filter(
        FieldPipeline.file_type == 'DELIVERY',
        FieldPipeline.target_col == 'D',
        FieldPipeline.enabled == True
    ).first()

    if pipeline:
        print(f"\n旧配置:")
        print(f"  target_col: {pipeline.target_col}")
        print(f"  target_header: {pipeline.target_header}")
        print(f"  map_op: {pipeline.map_op}")
        print(f"  source_cols: {pipeline.source_cols}")
        print(f"  depends_on: {pipeline.depends_on}")

        # 更新depends_on为C列（配達指定日）
        new_depends_on = '["配達指定日"]'  # JSON字符串格式
        pipeline.depends_on = new_depends_on

        print(f"\n新配置:")
        print(f"  target_col: {pipeline.target_col}")
        print(f"  target_header: {pipeline.target_header}")
        print(f"  map_op: {pipeline.map_op}")
        print(f"  source_cols: {pipeline.source_cols}")
        print(f"  depends_on: {pipeline.depends_on} (添加了对C列的依赖)")

        # 提交更改
        db.commit()

        print("\n" + "=" * 80)
        print("D列配置已更新，添加了对C列的依赖")
        print("=" * 80)
    else:
        print("\n未找到D列的配置")

except Exception as e:
    db.rollback()
    print(f"\n错误: {str(e)}")
    import traceback
    traceback.print_exc()
finally:
    db.close()
