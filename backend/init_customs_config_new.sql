-- 清关文件配置SQL语句（使用UPDATE方式）

-- 1. 更新或插入file_definitions配置（清关文件 - 源文件）
INSERT INTO file_definitions (id, file_type, file_role, sheet_name, header_row, data_start_row, columns_json, enabled, created_at, updated_at)
VALUES (
    UUID(),
    'CUSTOMS',
    'SOURCE',
    'Customs',
    1,
    2,
    '[{"col": "A", "header": "会员编号"}, {"col": "B", "header": "序号"}, {"col": "C", "header": "HAWB番号"}, {"col": "D", "header": "現地問合せ番号"}, {"col": "E", "header": "貨物個数"}, {"col": "F", "header": "貨物重量"}, {"col": "G", "header": "重量単位コード"}, {"col": "H", "header": "品名"}, {"col": "I", "header": "材质"}, {"col": "J", "header": "收件人名（删）"}, {"col": "K", "header": "輸入者名"}, {"col": "L", "header": "英文邮编录入(删)"}, {"col": "M", "header": "收件人地址(删)2"}, {"col": "N", "header": "輸入者住所（删）"}, {"col": "O", "header": "提取门牌(删)"}, {"col": "P", "header": "輸入者住所"}, {"col": "Q", "header": "輸入者 郵便番号"}, {"col": "R", "header": "輸入者電話番号"}, {"col": "S", "header": "輸出者名"}, {"col": "T", "header": "輸出者住所"}, {"col": "U", "header": "インボイス価格条件コード"}, {"col": "V", "header": "インボイス通貨コード"}, {"col": "W", "header": "インボイス価格"}, {"col": "X", "header": "单价（删）"}, {"col": "Y", "header": "運賃区分コード"}, {"col": "Z", "header": "運賃通貨コード"}, {"col": "AA", "header": "運賃"}, {"col": "AB", "header": "原産地コード"}, {"col": "AC", "header": "備考"}, {"col": "AD", "header": "收件人名（日文）"}, {"col": "AE", "header": "收件人地址"}, {"col": "AF", "header": "收件人电话"}, {"col": "AG", "header": "收件人邮编"}, {"col": "AH", "header": "依赖人名"}, {"col": "AI", "header": "依赖人地址"}, {"col": "AJ", "header": "依赖人电话"}, {"col": "AK", "header": "收件地址识别码"}, {"col": "AL", "header": "电商货识别码"}, {"col": "AM", "header": "电商平台码"}, {"col": "AN", "header": "电商平台名称"}, {"col": "AO", "header": ""}, {"col": "AP", "header": ""}, {"col": "AQ", "header": ""}, {"col": "AR", "header": ""}, {"col": "AS", "header": ""}, {"col": "AT", "header": ""}, {"col": "AU", "header": "单价（删）"}, {"col": "AV", "header": "发货地址（删）"}, {"col": "AW", "header": "发货省（删）"}, {"col": "AX", "header": "发货市（删）"}, {"col": "AY", "header": "收件人地址2（删）"}]',
    true,
    NOW(),
    NOW()
)
ON CONFLICT (file_type, file_role) DO UPDATE SET
    sheet_name = EXCLUDED.sheet_name,
    header_row = EXCLUDED.header_row,
    data_start_row = EXCLUDED.data_start_row,
    columns_json = EXCLUDED.columns_json,
    enabled = EXCLUDED.enabled,
    updated_at = NOW();

-- 2. 更新或插入file_definitions配置（清关文件 - 输出文件）
INSERT INTO file_definitions (id, file_type, file_role, sheet_name, header_row, data_start_row, columns_json, enabled, created_at, updated_at)
VALUES (
    UUID(),
    'CUSTOMS',
    'OUTPUT',
    'Customs',
    1,
    2,
    '[{"col": "A", "header": "会员编号"}, {"col": "B", "header": "序号"}, {"col": "C", "header": "HAWB番号"}, {"col": "D", "header": "現地問合せ番号"}, {"col": "E", "header": "貨物個数"}, {"col": "F", "header": "貨物重量"}, {"col": "G", "header": "重量単位コード"}, {"col": "H", "header": "品名"}, {"col": "I", "header": "材质"}, {"col": "J", "header": "輸入者名"}, {"col": "K", "header": "輸入者住所"}, {"col": "L", "header": "輸入者 郵便番号"}, {"col": "M", "header": "輸入者電話番号"}, {"col": "N", "header": "輸出者名"}, {"col": "O", "header": "輸出者住所"}, {"col": "P", "header": "インボイス価格条件コード"}, {"col": "Q", "header": "インボイス通貨コード"}, {"col": "R", "header": "インボイス価格"}, {"col": "S", "header": "運賃区分コード"}, {"col": "T", "header": "運賃通貨コード"}, {"col": "U", "header": "運賃"}, {"col": "V", "header": "原産地コード"}, {"col": "W", "header": "備考"}, {"col": "X", "header": "收件人名（日文）"}, {"col": "Y", "header": "收件人地址"}, {"col": "Z", "header": "收件人电话"}, {"col": "AA", "header": "收件人邮编"}, {"col": "AB", "header": "依赖人名"}, {"col": "AC", "header": "依赖人地址"}, {"col": "AD", "header": "依赖人电话"}, {"col": "AE", "header": "收件地址识别码"}, {"col": "AF", "header": "电商货识别码"}, {"col": "AG", "header": "电商平台码"}, {"col": "AH", "header": "电商平台名称"}, {"col": "AI", "header": ""}, {"col": "AJ", "header": ""}, {"col": "AK", "header": ""}, {"col": "AL", "header": ""}, {"col": "AM", "header": ""}, {"col": "AN", "header": ""}]',
    true,
    NOW(),
    NOW()
)
ON CONFLICT (file_type, file_role) DO UPDATE SET
    sheet_name = EXCLUDED.sheet_name,
    header_row = EXCLUDED.header_row,
    data_start_row = EXCLUDED.data_start_row,
    columns_json = EXCLUDED.columns_json,
    enabled = EXCLUDED.enabled,
    updated_at = NOW();

-- 3. 更新或插入field_pipelines配置（清关文件字段映射）
-- 使用INSERT IGNORE避免重复插入，忽略file_type, target_col冲突
INSERT IGNORE INTO field_pipelines
(id, file_type, target_col, target_header, map_op, source_cols, field_type, rule_ref, rule_params_json, depends_on, `order`, enabled, created_at, updated_at)
VALUES
-- A
(UUID(), 'CUSTOMS', 'A', '会员编号', 'COPY', '["会员编号"]', 'TEXT', '[]', NULL, '[]', 1, true, NOW(), NOW()),

-- B
(UUID(), 'CUSTOMS', 'B', '序号', 'NONE', '[]', 'NUMBER', '["seq_from_1"]', NULL, '[]', 2, true, NOW(), NOW()),

-- C / D
(UUID(), 'CUSTOMS', 'C', 'HAWB番号', 'COPY', '["HAWB番号"]', 'TEXT', '[]', NULL, '[]', 3, true, NOW(), NOW()),
(UUID(), 'CUSTOMS', 'D', '現地問合せ番号', 'COPY', '["現地問合せ番号"]', 'TEXT', '[]', NULL, '[]', 4, true, NOW(), NOW()),

-- E / F / G
(UUID(), 'CUSTOMS', 'E', '貨物個数', 'COPY', '["貨物個数"]', 'NUMBER', '[]', NULL, '[]', 5, true, NOW(), NOW()),
(UUID(), 'CUSTOMS', 'F', '貨物重量', 'NONE', '["貨物重量"]', 'NUMBER', '["ai_weight_infer"]', NULL, '[]', 6, true, NOW(), NOW()),
(UUID(), 'CUSTOMS', 'G', '重量単位コード', 'CONST', '[]', 'TEXT', '["const_value"]', '{"value":""}', '[]', 7, true, NOW(), NOW()),

-- H / I
(UUID(), 'CUSTOMS', 'H', '品名', 'NONE', '["品名"]', 'TEXT', '["ai_goods_name_en"]', NULL, '[]', 8, true, NOW(), NOW()),
(UUID(), 'CUSTOMS', 'I', '材质', 'NONE', '["材质"]', 'TEXT', '["ai_material_translate_and_map"]', NULL, '[]', 9, true, NOW(), NOW()),

-- J K L M
(UUID(), 'CUSTOMS', 'J', '輸入者名', 'COPY', '["輸入者名"]', 'TEXT', '[]', NULL, '[]', 10, true, NOW(), NOW()),
(UUID(), 'CUSTOMS', 'K', '輸入者住所', 'COPY', '["輸入者住所"]', 'TEXT', '[]', NULL, '[]', 11, true, NOW(), NOW()),
(UUID(), 'CUSTOMS', 'L', '輸入者 郵便番号', 'COPY', '["輸入者 郵便番号"]', 'TEXT', '[]', NULL, '[]', 12, true, NOW(), NOW()),
(UUID(), 'CUSTOMS', 'M', '輸入者電話番号', 'COPY', '["輸入者電話番号"]', 'TEXT', '[]', NULL, '[]', 13, true, NOW(), NOW()),

-- N O
(UUID(), 'CUSTOMS', 'N', '輸出者名', 'COPY', '["輸出者名"]', 'TEXT', '[]', NULL, '[]', 14, true, NOW(), NOW()),
(UUID(), 'CUSTOMS', 'O', '輸出者住所', 'COPY', '["輸出者住所"]', 'TEXT', '[]', NULL, '[]', 15, true, NOW(), NOW()),

-- P Q R
(UUID(), 'CUSTOMS', 'P', 'インボイス価格条件コード', 'COPY', '["インボイス価格条件コード"]', 'TEXT', '[]', NULL, '[]', 16, true, NOW(), NOW()),
(UUID(), 'CUSTOMS', 'Q', 'インボイス通貨コード', 'COPY', '["インボイス通貨コード"]', 'TEXT', '[]', NULL, '[]', 17, true, NOW(), NOW()),
(UUID(), 'CUSTOMS', 'R', 'インボイス価格', 'COPY', '["インボイス価格"]', 'NUMBER', '[]', NULL, '[]', 18, true, NOW(), NOW()),

-- S T U
(UUID(), 'CUSTOMS', 'S', '運賃区分コード', 'COPY', '["運賃区分コード"]', 'TEXT', '[]', NULL, '[]', 19, true, NOW(), NOW()),
(UUID(), 'CUSTOMS', 'T', '運賃通貨コード', 'COPY', '["運賃通貨コード"]', 'TEXT', '[]', NULL, '[]', 20, true, NOW(), NOW()),
(UUID(), 'CUSTOMS', 'U', '運賃', 'COPY', '["運賃"]', 'NUMBER', '[]', NULL, '[]', 21, true, NOW(), NOW()),

-- V W
(UUID(), 'CUSTOMS', 'V', '原産地コード', 'COPY', '["原産地コード"]', 'TEXT', '[]', NULL, '[]', 22, true, NOW(), NOW()),
(UUID(), 'CUSTOMS', 'W', '備考', 'COPY', '["備考"]', 'TEXT', '[]', NULL, '[]', 23, true, NOW(), NOW()),

-- X Y Z AA
(UUID(), 'CUSTOMS', 'X', '收件人名（日文）', 'COPY', '["收件人名（日文）"]', 'TEXT', '[]', NULL, '[]', 24, true, NOW(), NOW()),
(UUID(), 'CUSTOMS', 'Y', '收件人地址', 'COPY', '["收件人地址"]', 'TEXT', '[]', NULL, '[]', 25, true, NOW(), NOW()),
(UUID(), 'CUSTOMS', 'Z', '收件人电话', 'COPY', '["收件人电话"]', 'TEXT', '[]', NULL, '[]', 26, true, NOW(), NOW()),
(UUID(), 'CUSTOMS', 'AA', '收件人邮编', 'COPY', '["收件人邮编"]', 'TEXT', '[]', NULL, '[]', 27, true, NOW(), NOW()),

-- AB AC AD AE
(UUID(), 'CUSTOMS', 'AB', '依赖人名', 'COPY', '["依赖人名"]', 'TEXT', '[]', NULL, '[]', 28, true, NOW(), NOW()),
(UUID(), 'CUSTOMS', 'AC', '依赖人地址', 'COPY', '["依赖人地址"]', 'TEXT', '[]', NULL, '[]', 29, true, NOW(), NOW()),
(UUID(), 'CUSTOMS', 'AD', '依赖人电话', 'COPY', '["依赖人电话"]', 'TEXT', '[]', NULL, '[]', 30, true, NOW(), NOW()),
(UUID(), 'CUSTOMS', 'AE', '收件地址识别码', 'COPY', '["收件地址识别码"]', 'TEXT', '[]', NULL, '[]', 31, true, NOW(), NOW()),

-- AF AH AN
(UUID(), 'CUSTOMS', 'AF', '电商货识别码', 'COPY', '["电商货识别码"]', 'TEXT', '[]', NULL, '[]', 32, true, NOW(), NOW()),
(UUID(), 'CUSTOMS', 'AH', '电商平台码', 'COPY', '["电商平台码"]', 'TEXT', '[]', NULL, '[]', 33, true, NOW(), NOW()),
(UUID(), 'CUSTOMS', 'AN', '电商平台名称', 'COPY', '["电商平台名称"]', 'TEXT', '[]', NULL, '[]', 34, true, NOW(), NOW());

-- 禁用的字段（删除字段）
INSERT IGNORE INTO field_pipelines
(id, file_type, target_col, target_header, map_op, source_cols, field_type, rule_ref, rule_params_json, depends_on, `order`, enabled, created_at, updated_at)
VALUES
(UUID(), 'CUSTOMS', 'J', '收件人名（删）', 'COPY', '["收件人名（删）"]', 'TEXT', '[]', NULL, '[]', 35, false, NOW(), NOW()),
(UUID(), 'CUSTOMS', 'L', '英文邮编录入(删)', 'COPY', '["英文邮编录入(删)"]', 'TEXT', '[]', NULL, '[]', 36, false, NOW(), NOW()),
(UUID(), 'CUSTOMS', 'M', '收件人地址(删)2', 'COPY', '["收件人地址(删)2"]', 'TEXT', '[]', NULL, '[]', 37, false, NOW(), NOW()),
(UUID(), 'CUSTOMS', 'N', '輸入者住所（删）', 'COPY', '["輸入者住所（删）"]', 'TEXT', '[]', NULL, '[]', 38, false, NOW(), NOW()),
(UUID(), 'CUSTOMS', 'O', '提取门牌(删)', 'COPY', '["提取门牌(删)"]', 'TEXT', '[]', NULL, '[]', 39, false, NOW(), NOW()),
(UUID(), 'CUSTOMS', 'X', '单价（删）', 'COPY', '["单价（删）"]', 'NUMBER', '[]', NULL, '[]', 40, false, NOW(), NOW()),
(UUID(), 'CUSTOMS', 'AP', '收件人省州（删）', 'COPY', '["收件人省州（删）"]', 'TEXT', '[]', NULL, '[]', 41, false, NOW(), NOW()),
(UUID(), 'CUSTOMS', 'AQ', '收件人城市（删）', 'COPY', '["收件人城市（删）"]', 'TEXT', '[]', NULL, '[]', 42, false, NOW(), NOW()),
(UUID(), 'CUSTOMS', 'AR', '收件人地址（删）', 'COPY', '["收件人地址（删）"]', 'TEXT', '[]', NULL, '[]', 43, false, NOW(), NOW()),
(UUID(), 'CUSTOMS', 'AS', '申报品名（删）', 'COPY', '["申报品名（删）"]', 'TEXT', '[]', NULL, '[]', 44, false, NOW(), NOW()),
(UUID(), 'CUSTOMS', 'AT', '材质(删)', 'COPY', '["材质(删)"]', 'TEXT', '[]', NULL, '[]', 45, false, NOW(), NOW()),
(UUID(), 'CUSTOMS', 'AU', '单价（删）', 'COPY', '["单价（删）"]', 'NUMBER', '[]', NULL, '[]', 46, false, NOW(), NOW()),
(UUID(), 'CUSTOMS', 'AV', '发货地址（删）', 'COPY', '["发货地址（删）"]', 'TEXT', '[]', NULL, '[]', 47, false, NOW(), NOW()),
(UUID(), 'CUSTOMS', 'AW', '发货省（删）', 'COPY', '["发货省（删）"]', 'TEXT', '[]', NULL, '[]', 48, false, NOW(), NOW()),
(UUID(), 'CUSTOMS', 'AX', '发货市（删）', 'COPY', '["发货市（删）"]', 'TEXT', '[]', NULL, '[]', 49, false, NOW(), NOW()),
(UUID(), 'CUSTOMS', 'AY', '收件人地址2（删）', 'COPY', '["收件人地址2（删）"]', 'TEXT', '[]', NULL, '[]', 50, false, NOW(), NOW());