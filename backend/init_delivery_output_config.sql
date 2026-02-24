-- 派送文件结果文件配置SQL语句（使用UPDATE方式）

-- 1. 更新或插入file_definitions配置（派送文件 - 输出文件）
INSERT INTO file_definitions (file_type, file_role, sheet_name, header_row, data_start_row, columns_json, enabled, created_at, updated_at)
VALUES (
    'DELIVERY',
    'OUTPUT',
    'Delivery',
    1,
    2,
    '[{"col": "A", "header": "お客様管理番号"}, {"col": "B", "header": "佐川問合せ番号HAWB"}, {"col": "C", "header": "配達指定日"}, {"col": "D", "header": "時間帯指定"}, {"col": "E", "header": "貨物個数"}, {"col": "F", "header": "お届け先人名"}, {"col": "G", "header": "お届け先住所"}, {"col": "H", "header": "お届け先電話"}, {"col": "I", "header": "お届け先郵便"}, {"col": "J", "header": "依頼主"}, {"col": "K", "header": "依頼主住所"}, {"col": "L", "header": "依頼主郵便番号"}, {"col": "M", "header": "依頼主電話"}, {"col": "N", "header": "佐川顧客コード（固定）"}, {"col": "O", "header": "記事欄2（品名）"}, {"col": "P", "header": "記事欄2"}, {"col": "Q", "header": "記事欄3"}]',
    true,
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP
)
ON CONFLICT (file_type, file_role) DO UPDATE SET
    sheet_name = EXCLUDED.sheet_name,
    header_row = EXCLUDED.header_row,
    data_start_row = EXCLUDED.data_start_row,
    columns_json = EXCLUDED.columns_json,
    enabled = EXCLUDED.enabled,
    updated_at = CURRENT_TIMESTAMP;

-- 2. 更新或插入field_pipelines配置（派送文件字段映射）

-- お客様管理番号
INSERT INTO field_pipelines (file_type, target_col, target_header, map_op, source_cols, field_type, rule_ref, depends_on, order, enabled, created_at, updated_at)
VALUES ('DELIVERY', 'A', 'お客様管理番号', 'COPY', '["お客様管理番号"]', 'TEXT', '[]', '[]', 1, true, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
ON CONFLICT (file_type, target_col) DO UPDATE SET
    target_header = EXCLUDED.target_header,
    map_op = EXCLUDED.map_op,
    source_cols = EXCLUDED.source_cols,
    field_type = EXCLUDED.field_type,
    rule_ref = EXCLUDED.rule_ref,
    depends_on = EXCLUDED.depends_on,
    order = EXCLUDED.order,
    enabled = EXCLUDED.enabled,
    updated_at = CURRENT_TIMESTAMP;

-- 佐川問合せ番号HAWB
INSERT INTO field_pipelines (file_type, target_col, target_header, map_op, source_cols, field_type, rule_ref, depends_on, order, enabled, created_at, updated_at)
VALUES ('DELIVERY', 'B', '佐川問合せ番号HAWB', 'COPY', '["HAWB番号"]', 'TEXT', '[]', '[]', 2, true, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
ON CONFLICT (file_type, target_col) DO UPDATE SET
    target_header = EXCLUDED.target_header,
    map_op = EXCLUDED.map_op,
    source_cols = EXCLUDED.source_cols,
    field_type = EXCLUDED.field_type,
    rule_ref = EXCLUDED.rule_ref,
    depends_on = EXCLUDED.depends_on,
    order = EXCLUDED.order,
    enabled = EXCLUDED.enabled,
    updated_at = CURRENT_TIMESTAMP;

-- 配達指定日
INSERT INTO field_pipelines (file_type, target_col, target_header, map_op, source_cols, field_type, rule_ref, depends_on, order, enabled, created_at, updated_at)
VALUES ('DELIVERY', 'C', '配達指定日', 'COPY', '["配達指定日"]', 'TEXT', '[]', '[]', 3, true, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
ON CONFLICT (file_type, target_col) DO UPDATE SET
    target_header = EXCLUDED.target_header,
    map_op = EXCLUDED.map_op,
    source_cols = EXCLUDED.source_cols,
    field_type = EXCLUDED.field_type,
    rule_ref = EXCLUDED.rule_ref,
    depends_on = EXCLUDED.depends_on,
    order = EXCLUDED.order,
    enabled = EXCLUDED.enabled,
    updated_at = CURRENT_TIMESTAMP;

-- 時間帯指定
INSERT INTO field_pipelines (file_type, target_col, target_header, map_op, source_cols, field_type, rule_ref, depends_on, order, enabled, created_at, updated_at)
VALUES ('DELIVERY', 'D', '時間帯指定', 'COPY', '["時間帯指定"]', 'TEXT', '[]', '[]', 4, true, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
ON CONFLICT (file_type, target_col) DO UPDATE SET
    target_header = EXCLUDED.target_header,
    map_op = EXCLUDED.map_op,
    source_cols = EXCLUDED.source_cols,
    field_type = EXCLUDED.field_type,
    rule_ref = EXCLUDED.rule_ref,
    depends_on = EXCLUDED.depends_on,
    order = EXCLUDED.order,
    enabled = EXCLUDED.enabled,
    updated_at = CURRENT_TIMESTAMP;

-- 貨物個数
INSERT INTO field_pipelines (file_type, target_col, target_header, map_op, source_cols, field_type, rule_ref, depends_on, order, enabled, created_at, updated_at)
VALUES ('DELIVERY', 'E', '貨物個数', 'COPY', '["貨物個数"]', 'NUMBER', '[]', '[]', 5, true, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
ON CONFLICT (file_type, target_col) DO UPDATE SET
    target_header = EXCLUDED.target_header,
    map_op = EXCLUDED.map_op,
    source_cols = EXCLUDED.source_cols,
    field_type = EXCLUDED.field_type,
    rule_ref = EXCLUDED.rule_ref,
    depends_on = EXCLUDED.depends_on,
    order = EXCLUDED.order,
    enabled = EXCLUDED.enabled,
    updated_at = CURRENT_TIMESTAMP;

-- お届け先人名
INSERT INTO field_pipelines (file_type, target_col, target_header, map_op, source_cols, field_type, rule_ref, depends_on, order, enabled, created_at, updated_at)
VALUES ('DELIVERY', 'F', 'お届け先人名', 'COPY', '["お届け先人名"]', 'TEXT', '[]', '[]', 6, true, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
ON CONFLICT (file_type, target_col) DO UPDATE SET
    target_header = EXCLUDED.target_header,
    map_op = EXCLUDED.map_op,
    source_cols = EXCLUDED.source_cols,
    field_type = EXCLUDED.field_type,
    rule_ref = EXCLUDED.rule_ref,
    depends_on = EXCLUDED.depends_on,
    order = EXCLUDED.order,
    enabled = EXCLUDED.enabled,
    updated_at = CURRENT_TIMESTAMP;

-- お届け先住所
INSERT INTO field_pipelines (file_type, target_col, target_header, map_op, source_cols, field_type, rule_ref, depends_on, order, enabled, created_at, updated_at)
VALUES ('DELIVERY', 'G', 'お届け先住所', 'COPY', '["お届け先住所"]', 'TEXT', '[]', '[]', 7, true, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
ON CONFLICT (file_type, target_col) DO UPDATE SET
    target_header = EXCLUDED.target_header,
    map_op = EXCLUDED.map_op,
    source_cols = EXCLUDED.source_cols,
    field_type = EXCLUDED.field_type,
    rule_ref = EXCLUDED.rule_ref,
    depends_on = EXCLUDED.depends_on,
    order = EXCLUDED.order,
    enabled = EXCLUDED.enabled,
    updated_at = CURRENT_TIMESTAMP;

-- お届け先電話
INSERT INTO field_pipelines (file_type, target_col, target_header, map_op, source_cols, field_type, rule_ref, depends_on, order, enabled, created_at, updated_at)
VALUES ('DELIVERY', 'H', 'お届け先電話', 'COPY', '["お届け先電話"]', 'TEXT', '[]', '[]', 8, true, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
ON CONFLICT (file_type, target_col) DO UPDATE SET
    target_header = EXCLUDED.target_header,
    map_op = EXCLUDED.map_op,
    source_cols = EXCLUDED.source_cols,
    field_type = EXCLUDED.field_type,
    rule_ref = EXCLUDED.rule_ref,
    depends_on = EXCLUDED.depends_on,
    order = EXCLUDED.order,
    enabled = EXCLUDED.enabled,
    updated_at = CURRENT_TIMESTAMP;

-- お届け先郵便
INSERT INTO field_pipelines (file_type, target_col, target_header, map_op, source_cols, field_type, rule_ref, depends_on, order, enabled, created_at, updated_at)
VALUES ('DELIVERY', 'I', 'お届け先郵便', 'COPY', '["お届け先郵便"]', 'TEXT', '[]', '[]', 9, true, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
ON CONFLICT (file_type, target_col) DO UPDATE SET
    target_header = EXCLUDED.target_header,
    map_op = EXCLUDED.map_op,
    source_cols = EXCLUDED.source_cols,
    field_type = EXCLUDED.field_type,
    rule_ref = EXCLUDED.rule_ref,
    depends_on = EXCLUDED.depends_on,
    order = EXCLUDED.order,
    enabled = EXCLUDED.enabled,
    updated_at = CURRENT_TIMESTAMP;

-- 依頼主
INSERT INTO field_pipelines (file_type, target_col, target_header, map_op, source_cols, field_type, rule_ref, depends_on, order, enabled, created_at, updated_at)
VALUES ('DELIVERY', 'J', '依頼主', 'COPY', '["依頼主"]', 'TEXT', '[]', '[]', 10, true, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
ON CONFLICT (file_type, target_col) DO UPDATE SET
    target_header = EXCLUDED.target_header,
    map_op = EXCLUDED.map_op,
    source_cols = EXCLUDED.source_cols,
    field_type = EXCLUDED.field_type,
    rule_ref = EXCLUDED.rule_ref,
    depends_on = EXCLUDED.depends_on,
    order = EXCLUDED.order,
    enabled = EXCLUDED.enabled,
    updated_at = CURRENT_TIMESTAMP;

-- 依頼主住所
INSERT INTO field_pipelines (file_type, target_col, target_header, map_op, source_cols, field_type, rule_ref, depends_on, order, enabled, created_at, updated_at)
VALUES ('DELIVERY', 'K', '依頼主住所', 'COPY', '["依頼主住所"]', 'TEXT', '[]', '[]', 11, true, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
ON CONFLICT (file_type, target_col) DO UPDATE SET
    target_header = EXCLUDED.target_header,
    map_op = EXCLUDED.map_op,
    source_cols = EXCLUDED.source_cols,
    field_type = EXCLUDED.field_type,
    rule_ref = EXCLUDED.rule_ref,
    depends_on = EXCLUDED.depends_on,
    order = EXCLUDED.order,
    enabled = EXCLUDED.enabled,
    updated_at = CURRENT_TIMESTAMP;

-- 依頼主郵便番号
INSERT INTO field_pipelines (file_type, target_col, target_header, map_op, source_cols, field_type, rule_ref, depends_on, order, enabled, created_at, updated_at)
VALUES ('DELIVERY', 'L', '依頼主郵便番号', 'COPY', '["依頼主郵便番号"]', 'TEXT', '[]', '[]', 12, true, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
ON CONFLICT (file_type, target_col) DO UPDATE SET
    target_header = EXCLUDED.target_header,
    map_op = EXCLUDED.map_op,
    source_cols = EXCLUDED.source_cols,
    field_type = EXCLUDED.field_type,
    rule_ref = EXCLUDED.rule_ref,
    depends_on = EXCLUDED.depends_on,
    order = EXCLUDED.order,
    enabled = EXCLUDED.enabled,
    updated_at = CURRENT_TIMESTAMP;

-- 依頼主電話
INSERT INTO field_pipelines (file_type, target_col, target_header, map_op, source_cols, field_type, rule_ref, depends_on, order, enabled, created_at, updated_at)
VALUES ('DELIVERY', 'M', '依頼主電話', 'COPY', '["依頼主電話"]', 'TEXT', '[]', '[]', 13, true, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
ON CONFLICT (file_type, target_col) DO UPDATE SET
    target_header = EXCLUDED.target_header,
    map_op = EXCLUDED.map_op,
    source_cols = EXCLUDED.source_cols,
    field_type = EXCLUDED.field_type,
    rule_ref = EXCLUDED.rule_ref,
    depends_on = EXCLUDED.depends_on,
    order = EXCLUDED.order,
    enabled = EXCLUDED.enabled,
    updated_at = CURRENT_TIMESTAMP;

-- 佐川顧客コード（固定）
INSERT INTO field_pipelines (file_type, target_col, target_header, map_op, source_cols, field_type, rule_ref, depends_on, order, enabled, created_at, updated_at)
VALUES ('DELIVERY', 'N', '佐川顧客コード（固定）', 'CONST', '[]', 'TEXT', '[]', '[]', 14, true, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
ON CONFLICT (file_type, target_col) DO UPDATE SET
    target_header = EXCLUDED.target_header,
    map_op = EXCLUDED.map_op,
    source_cols = EXCLUDED.source_cols,
    field_type = EXCLUDED.field_type,
    rule_ref = EXCLUDED.rule_ref,
    depends_on = EXCLUDED.depends_on,
    order = EXCLUDED.order,
    enabled = EXCLUDED.enabled,
    updated_at = CURRENT_TIMESTAMP;

-- 記事欄2（品名）
INSERT INTO field_pipelines (file_type, target_col, target_header, map_op, source_cols, field_type, rule_ref, depends_on, order, enabled, created_at, updated_at)
VALUES ('DELIVERY', 'O', '記事欄2（品名）', 'COPY', '["品名"]', 'TEXT', '[]', '[]', 15, true, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
ON CONFLICT (file_type, target_col) DO UPDATE SET
    target_header = EXCLUDED.target_header,
    map_op = EXCLUDED.map_op,
    source_cols = EXCLUDED.source_cols,
    field_type = EXCLUDED.field_type,
    rule_ref = EXCLUDED.rule_ref,
    depends_on = EXCLUDED.depends_on,
    order = EXCLUDED.order,
    enabled = EXCLUDED.enabled,
    updated_at = CURRENT_TIMESTAMP;

-- 記事欄2
INSERT INTO field_pipelines (file_type, target_col, target_header, map_op, source_cols, field_type, rule_ref, depends_on, order, enabled, created_at, updated_at)
VALUES ('DELIVERY', 'P', '記事欄2', 'COPY', '["記事欄2"]', 'TEXT', '[]', '[]', 16, true, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
ON CONFLICT (file_type, target_col) DO UPDATE SET
    target_header = EXCLUDED.target_header,
    map_op = EXCLUDED.map_op,
    source_cols = EXCLUDED.source_cols,
    field_type = EXCLUDED.field_type,
    rule_ref = EXCLUDED.rule_ref,
    depends_on = EXCLUDED.depends_on,
    order = EXCLUDED.order,
    enabled = EXCLUDED.enabled,
    updated_at = CURRENT_TIMESTAMP;

-- 記事欄3
INSERT INTO field_pipelines (file_type, target_col, target_header, map_op, source_cols, field_type, rule_ref, depends_on, order, enabled, created_at, updated_at)
VALUES ('DELIVERY', 'Q', '記事欄3', 'COPY', '["記事欄3"]', 'TEXT', '[]', '[]', 17, true, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
ON CONFLICT (file_type, target_col) DO UPDATE SET
    target_header = EXCLUDED.target_header,
    map_op = EXCLUDED.map_op,
    source_cols = EXCLUDED.source_cols,
    field_type = EXCLUDED.field_type,
    rule_ref = EXCLUDED.rule_ref,
    depends_on = EXCLUDED.depends_on,
    order = EXCLUDED.order,
    enabled = EXCLUDED.enabled,
    updated_at = CURRENT_TIMESTAMP;
