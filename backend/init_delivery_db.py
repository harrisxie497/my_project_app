"""初始化DELIVERY配置到数据库"""
from app.core.database import SessionLocal
from app.models.file_definition import FileDefinition
from app.models.field_pipeline import FieldPipeline
import json

db = SessionLocal()

# 创建DELIVERY SOURCE file_definition
source_columns = [
    {"col": "A", "header": "お客様管理番号"},
    {"col": "B", "header": "佐川問合せ番号HAWB"},
    {"col": "C", "header": "配達指定日"},
    {"col": "D", "header": "時間帯指定"},
    {"col": "E", "header": "貨物個数"},
    {"col": "F", "header": "お届け先人名"},
    {"col": "G", "header": "お届け先住所"},
    {"col": "H", "header": "お届け先電話"},
    {"col": "I", "header": "お届け先郵便"},
    {"col": "J", "header": "依頼主"},
    {"col": "K", "header": "依頼主住所"},
    {"col": "L", "header": "依頼主郵便番号"},
    {"col": "M", "header": "依頼主電話"},
    {"col": "N", "header": "佐川顧客コード（固定）"},
    {"col": "O", "header": "記事欄2（品名）"},
    {"col": "P", "header": "記事欄2"},
    {"col": "Q", "header": "記事欄3"},
    {"col": "R", "header": "收件人省州（删）"},
    {"col": "S", "header": "收件人城市（删）"},
    {"col": "T", "header": "收件人地址1（删）"},
    {"col": "U", "header": "收件人地址2（删）"},
    {"col": "V", "header": "発貨省（删）"},
    {"col": "W", "header": "発貨市（删）"},
    {"col": "X", "header": "発貨住所（删）"}
]

fd_source = FileDefinition(
    file_type='DELIVERY',
    file_role='SOURCE',
    sheet_name='Delivery',
    header_row=1,
    data_start_row=2,
    columns_json=json.dumps(source_columns),
    enabled=True
)
db.merge(fd_source)
print('DELIVERY SOURCE created')

# 创建DELIVERY OUTPUT file_definition
output_columns = source_columns[:17]  # 只保留A-Q列
fd_output = FileDefinition(
    file_type='DELIVERY',
    file_role='OUTPUT',
    sheet_name='Delivery',
    header_row=1,
    data_start_row=2,
    columns_json=json.dumps(output_columns),
    enabled=True
)
db.merge(fd_output)
print('DELIVERY OUTPUT created')

db.close()
