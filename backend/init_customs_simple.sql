-- 清关文件配置SQL语句（简化版）

-- 1. 插入file_definitions配置（清关文件 - 源文件）
INSERT INTO file_definitions (id, file_type, file_role, sheet_name, header_row, data_start_row, columns_json, enabled, created_at, updated_at)
VALUES (
    UUID(),
    'CUSTOMS',
    'SOURCE',
    'Customs',
    1,
    2,
    '[{"col": "A", "header": "会员编号"}]',
    1,
    NOW(),
    NOW());

-- 2. 插入file_definitions配置（清关文件 - 输出文件）
INSERT INTO file_definitions (id, file_type, file_role, sheet_name, header_row, data_start_row, columns_json, enabled, created_at, updated_at)
VALUES (
    UUID(),
    'CUSTOMS',
    'OUTPUT',
    'Customs',
    1,
    2,
    '[{"col": "A", "header": "会员编号"}]',
    1,
    NOW(),
    NOW());

-- 3. 插入field_pipelines配置（清关文件字段映射）
-- 启用的字段（前10个）
INSERT IGNORE INTO field_pipelines (id, file_type, target_col, target_header, map_op, source_cols, field_type, rule_ref, depends_on, `order`, enabled, created_at, updated_at)
VALUES
(UUID(), 'CUSTOMS', 'A', '会员编号', 'COPY', '["会员编号"]', 'TEXT', '[]', '[]', 1, true, NOW(), NOW()),
(UUID(), 'CUSTOMS', 'B', '序号', 'NONE', '[]', 'NUMBER', '["seq_from_1"]', '[]', 2, true, NOW(), NOW()),
(UUID(), 'CUSTOMS', 'C', 'HAWB番号', 'COPY', '["HAWB番号"]', 'TEXT', '[]', '[]', 3, true, NOW(), NOW()),
(UUID(), 'CUSTOMS', 'D', '現地問合せ番号', 'COPY', '["現地問合せ番号"]', 'TEXT', '[]', '[]', 4, true, NOW(), NOW()),
(UUID(), 'CUSTOMS', 'E', '貨物個数', 'COPY', '["貨物個数"]', 'NUMBER', '[]', '[]', 5, true, NOW(), NOW()),
(UUID(), 'CUSTOMS', 'F', '貨物重量', 'NONE', '["貨物重量"]', 'NUMBER', '["ai_weight_infer"]', '[]', 6, true, NOW(), NOW()),
(UUID(), 'CUSTOMS', 'G', '重量単位コード', 'CONST', '[]', 'TEXT', '["const_value"]', '[]', 7, true, NOW(), NOW()),
(UUID(), 'CUSTOMS', 'H', '品名', 'NONE', '["品名"]', 'TEXT', '["ai_goods_name_en"]', '[]', 8, true, NOW(), NOW()),
(UUID(), 'CUSTOMS', 'I', '材质', 'NONE', '["材质"]', 'TEXT', '["ai_material_translate_and_map"]', '[]', 9, true, NOW(), NOW()),
(UUID(), 'CUSTOMS', 'J', '輸入者名', 'COPY', '["輸入者名"]', 'TEXT', '[]', '[]', 10, true, NOW(), NOW());

-- 禁用的字段
INSERT IGNORE INTO field_pipelines (id, file_type, target_col, target_header, map_op, source_cols, field_type, rule_ref, depends_on, `order`, enabled, created_at, updated_at)
VALUES
(UUID(), 'CUSTOMS', 'L', '英文邮编录入(删)', 'COPY', '["英文邮编录入(删)"]', 'TEXT', '[]', '[]', 36, false, NOW(), NOW()),
(UUID(), 'CUSTOMS', 'M', '收件人地址(删)2', 'COPY', '["收件人地址(删)2"]', 'TEXT', '[]', '[]', 37, false, NOW(), NOW());