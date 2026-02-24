"""初始化DELIVERY field_pipelines到数据库"""
from app.core.database import SessionLocal
from app.models.field_pipeline import FieldPipeline

db = SessionLocal()

# DELIVERY field_pipelines配置
pipelines = [
    # お客様管理番号
    {
        'file_type': 'DELIVERY',
        'target_col': 'A',
        'target_header': 'お客様管理番号',
        'map_op': 'COPY',
        'source_cols': '["お客様管理番号"]',
        'field_type': 'TEXT',
        'rule_ref': '[]',
        'depends_on': '[]',
        'order_num': 1,
        'enabled': 1
    },
    # 佐川問合せ番号HAWB
    {
        'file_type': 'DELIVERY',
        'target_col': 'B',
        'target_header': '佐川問合せ番号HAWB',
        'map_op': 'COPY',
        'source_cols': '["佐川問合せ番号HAWB"]',
        'field_type': 'TEXT',
        'rule_ref': '[]',
        'depends_on': '[]',
        'order_num': 2,
        'enabled': 1
    },
    # 配達指定日
    {
        'file_type': 'DELIVERY',
        'target_col': 'C',
        'target_header': '配達指定日',
        'map_op': 'COPY',
        'source_cols': '["配達指定日"]',
        'field_type': 'TEXT',
        'rule_ref': '[]',
        'depends_on': '[]',
        'order_num': 3,
        'enabled': 1
    },
    # 時間帯指定
    {
        'file_type': 'DELIVERY',
        'target_col': 'D',
        'target_header': '時間帯指定',
        'map_op': 'COPY',
        'source_cols': '["時間帯指定"]',
        'field_type': 'TEXT',
        'rule_ref': '[]',
        'depends_on': '[]',
        'order_num': 4,
        'enabled': 1
    },
    # 貨物個数
    {
        'file_type': 'DELIVERY',
        'target_col': 'E',
        'target_header': '貨物個数',
        'map_op': 'COPY',
        'source_cols': '["貨物個数"]',
        'field_type': 'NUMBER',
        'rule_ref': '[]',
        'depends_on': '[]',
        'order_num': 5,
        'enabled': 1
    },
    # お届け先人名
    {
        'file_type': 'DELIVERY',
        'target_col': 'F',
        'target_header': 'お届け先人名',
        'map_op': 'COPY',
        'source_cols': '["お届け先人名"]',
        'field_type': 'TEXT',
        'rule_ref': '[]',
        'depends_on': '[]',
        'order_num': 6,
        'enabled': 1
    },
    # お届け先住所
    {
        'file_type': 'DELIVERY',
        'target_col': 'G',
        'target_header': 'お届け先住所',
        'map_op': 'COPY',
        'source_cols': '["お届け先住所"]',
        'field_type': 'TEXT',
        'rule_ref': '[]',
        'depends_on': '[]',
        'order_num': 7,
        'enabled': 1
    },
    # お届け先電話
    {
        'file_type': 'DELIVERY',
        'target_col': 'H',
        'target_header': 'お届け先電話',
        'map_op': 'COPY',
        'source_cols': '["お届け先電話"]',
        'field_type': 'TEXT',
        'rule_ref': '[]',
        'depends_on': '[]',
        'order_num': 8,
        'enabled': 1
    },
    # お届け先郵便
    {
        'file_type': 'DELIVERY',
        'target_col': 'I',
        'target_header': 'お届け先郵便',
        'map_op': 'COPY',
        'source_cols': '["お届け先郵便"]',
        'field_type': 'TEXT',
        'rule_ref': '[]',
        'depends_on': '[]',
        'order_num': 9,
        'enabled': 1
    },
    # 依頼主
    {
        'file_type': 'DELIVERY',
        'target_col': 'J',
        'target_header': '依頼主',
        'map_op': 'COPY',
        'source_cols': '["依頼主"]',
        'field_type': 'TEXT',
        'rule_ref': '[]',
        'depends_on': '[]',
        'order_num': 10,
        'enabled': 1
    },
    # 依頼主住所
    {
        'file_type': 'DELIVERY',
        'target_col': 'K',
        'target_header': '依頼主住所',
        'map_op': 'COPY',
        'source_cols': '["依頼主住所"]',
        'field_type': 'TEXT',
        'rule_ref': '[]',
        'depends_on': '[]',
        'order_num': 11,
        'enabled': 1
    },
    # 依頼主郵便番号
    {
        'file_type': 'DELIVERY',
        'target_col': 'L',
        'target_header': '依頼主郵便番号',
        'map_op': 'COPY',
        'source_cols': '["依頼主郵便番号"]',
        'field_type': 'TEXT',
        'rule_ref': '[]',
        'depends_on': '[]',
        'order_num': 12,
        'enabled': 1
    },
    # 依頼主電話
    {
        'file_type': 'DELIVERY',
        'target_col': 'M',
        'target_header': '依頼主電話',
        'map_op': 'COPY',
        'source_cols': '["依頼主電話"]',
        'field_type': 'TEXT',
        'rule_ref': '[]',
        'depends_on': '[]',
        'order_num': 13,
        'enabled': 1
    },
    # 佐川顧客コード（固定）
    {
        'file_type': 'DELIVERY',
        'target_col': 'N',
        'target_header': '佐川顧客コード（固定）',
        'map_op': 'CONST',
        'source_cols': '[]',
        'field_type': 'TEXT',
        'rule_ref': '[]',
        'depends_on': '[]',
        'order_num': 14,
        'enabled': 1
    },
    # 記事欄2（品名）
    {
        'file_type': 'DELIVERY',
        'target_col': 'O',
        'target_header': '記事欄2（品名）',
        'map_op': 'COPY',
        'source_cols': '["記事欄2（品名）"]',
        'field_type': 'TEXT',
        'rule_ref': '[]',
        'depends_on': '[]',
        'order_num': 15,
        'enabled': 1
    },
    # 記事欄2
    {
        'file_type': 'DELIVERY',
        'target_col': 'P',
        'target_header': '記事欄2',
        'map_op': 'COPY',
        'source_cols': '["記事欄2"]',
        'field_type': 'TEXT',
        'rule_ref': '[]',
        'depends_on': '[]',
        'order_num': 16,
        'enabled': 1
    },
    # 記事欄3
    {
        'file_type': 'DELIVERY',
        'target_col': 'Q',
        'target_header': '記事欄3',
        'map_op': 'COPY',
        'source_cols': '["記事欄3"]',
        'field_type': 'TEXT',
        'rule_ref': '[]',
        'depends_on': '[]',
        'order_num': 17,
        'enabled': 1
    }
]

for p in pipelines:
    fp = FieldPipeline(**p)
    db.merge(fp)
    print(f"Created pipeline: {p['target_col']} -> {p['target_header']}")

db.commit()
db.close()
print(f"Total {len(pipelines)} pipelines created for DELIVERY")
