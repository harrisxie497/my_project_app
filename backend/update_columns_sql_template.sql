-- DELIVERY file_definitions columns_json 更新SQL模板

-- 1. 更新SOURCE配置（25列）
UPDATE file_definitions
SET columns_json = '[
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
    {"col": "V", "header": "收件人地址3（删）"},
    {"col": "W", "header": "发货省（删）"},
    {"col": "X", "header": "发货市（删）"},
    {"col": "Y", "header": "发货地址（删）"}
]'::jsonb,
    updated_at = NOW()
WHERE file_type = 'DELIVERY'
  AND file_role = 'SOURCE';

-- 2. 更新OUTPUT配置（17列）
UPDATE file_definitions
SET columns_json = '[
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
    {"col": "Q", "header": "記事欄3"}
]'::jsonb,
    updated_at = NOW()
WHERE file_type = 'DELIVERY'
  AND file_role = 'OUTPUT';

-- 验证更新结果
SELECT file_role, sheet_name, jsonb_array_length(columns_json) as column_count, updated_at
FROM file_definitions
WHERE file_type = 'DELIVERY';
