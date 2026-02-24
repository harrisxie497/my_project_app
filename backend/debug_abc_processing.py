"""
调试A、B、C列的处理过程
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.core.database import SessionLocal
from app.services.excel_reader import read_excel_file
from app.models.field_pipeline import FieldPipeline
import json

print("=" * 80)
print("调试A、B、C列的处理过程")
print("=" * 80)

# 读取原始文件
original_file = "storage/tasks/test_abc_columns_001/original.xlsx"
result = read_excel_file(original_file, file_type='DELIVERY', file_role='SOURCE')

column_data = result['column_data']

# 构建column_data_map（模拟delivery_processor的逻辑）
header_to_col_letter = {}
col_letter_to_data = {}
for col in column_data:
    col_source_cols = col.get('source_cols')
    col_header = col.get('head')
    if col_source_cols:
        col_letter_to_data[col_source_cols] = col.get('data')
        if col_header:
            header_to_col_letter[col_header] = col_source_cols

column_data_map = {}
for header, col_letter in header_to_col_letter.items():
    if col_letter in col_letter_to_data:
        column_data_map[header] = col_letter_to_data[col_letter]

print("\n【column_data_map构建结果】")
print("-" * 80)

# 检查A、B、C列
abc_headers = ['お客様管理番号', '佐川問合せ番号HAWB', '配達指定日']
for header in abc_headers:
    if header in column_data_map:
        data = column_data_map[header]
        print(f"\n{header}:")
        print(f"  数据长度: {len(data)}")
        print(f"  数据内容: {data}")
    else:
        print(f"\n{header}: 未在column_data_map中找到")

# 检查field_pipelines配置
print("\n\n【field_pipelines配置】")
print("-" * 80)

db = SessionLocal()
try:
    pipelines = db.query(FieldPipeline).filter(
        FieldPipeline.file_type == 'DELIVERY',
        FieldPipeline.enabled == True
    ).order_by(FieldPipeline.order_num).all()

    for pipeline in pipelines:
        target_col = pipeline.target_col
        target_header = pipeline.target_header
        map_op = pipeline.map_op
        source_cols = pipeline.source_cols

        if target_col in ['A', 'B', 'C']:
            print(f"\n列 {target_col} ({target_header}):")
            print(f"  map_op: {map_op}")
            print(f"  source_cols: {source_cols}")
            print(f"  source_cols 类型: {type(source_cols)}")

            # 检查source_cols在column_data_map中是否存在
            if isinstance(source_cols, list):
                print(f"  source_cols 是列表，长度: {len(source_cols)}")
                for source_col in source_cols:
                    if source_col in column_data_map:
                        print(f"  source_col '{source_col}' 在 column_data_map 中: YES")
                    else:
                        print(f"  source_col '{source_col}' 在 column_data_map 中: NO")
            elif isinstance(source_cols, str):
                print(f"  source_cols 是字符串，需要解析为JSON")
                try:
                    import json
                    parsed_cols = json.loads(source_cols)
                    print(f"  解析后的source_cols: {parsed_cols}")
                    for source_col in parsed_cols:
                        if source_col in column_data_map:
                            print(f"  source_col '{source_col}' 在 column_data_map 中: YES")
                        else:
                            print(f"  source_col '{source_col}' 在 column_data_map 中: NO")
                except Exception as e:
                    print(f"  解析JSON失败: {e}")
            else:
                print(f"  source_cols 类型异常: {type(source_cols)}")
finally:
    db.close()
