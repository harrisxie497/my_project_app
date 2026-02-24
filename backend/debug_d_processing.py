"""
调试D列的处理过程
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.core.database import SessionLocal
from app.services.delivery_processor import DeliveryProcessor
import openpyxl

print("=" * 80)
print("调试D列的处理过程")
print("=" * 80)

# 测试任务目录
task_dir = "storage/tasks/test_d_column_001"

# 创建数据库会话
db = SessionLocal()

try:
    print("\n【步骤1】处理文件")
    print("-" * 80)

    header_params = {
        'mawb_no': '160-03270890',
        'flight_no': 'CA123',
        'arrival_date': '2026-02-10'
    }

    processor = DeliveryProcessor(
        task_dir=task_dir,
        db_session=db,
        file_type='DELIVERY',
        header_params=header_params
    )

    result = processor.process()

    print("\n【步骤2】检查processed_column_data中的D列数据")
    print("-" * 80)

    # 手动读取处理后的数据
    from app.services.excel_reader import read_excel_file
    original_result = read_excel_file(
        os.path.join(task_dir, "original.xlsx"),
        file_type='DELIVERY',
        file_role='SOURCE'
    )

    # 获取field_pipelines配置
    from app.models.field_pipeline import FieldPipeline
    pipelines = db.query(FieldPipeline).filter(
        FieldPipeline.file_type == 'DELIVERY',
        FieldPipeline.enabled == True
    ).order_by(FieldPipeline.order_num).all()

    # 找到D列的配置
    d_pipeline = None
    for p in pipelines:
        if p.target_col == 'D':
            d_pipeline = p
            break

    if d_pipeline:
        print(f"D列配置:")
        print(f"  target_col: {d_pipeline.target_col}")
        print(f"  map_op: {d_pipeline.map_op}")
        print(f"  source_cols: {d_pipeline.source_cols}")
        print(f"  depends_on: {d_pipeline.depends_on}")

    # 手动处理D列
    from app.services.field_handlers import calc_time_slot_with_delivery_date
    import json

    d_col_data = None
    for col in original_result['column_data']:
        if col.get('head') == '時間帯指定':
            d_col_data = col.get('data')
            break

    c_col_data = None
    for col in original_result['column_data']:
        if col.get('head') == '配達指定日':
            c_col_data = col.get('data')
            break

    print(f"\n原始D列数据: {d_col_data}")
    print(f"原始C列数据: {c_col_data}")

    print(f"\n手动处理D列:")
    for idx in range(len(d_col_data)):
        d_val = d_col_data[idx]
        c_val = c_col_data[idx] if idx < len(c_col_data) else None
        processed_val = calc_time_slot_with_delivery_date(d_val, c_val)
        print(f"  第{idx+2}行: D={repr(d_val)}, C={repr(c_val)} -> {repr(processed_val)}")

except Exception as e:
    print(f"\n错误: {str(e)}")
    import traceback
    traceback.print_exc()
finally:
    db.close()
