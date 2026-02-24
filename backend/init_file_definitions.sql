-- file_definitions 表统一初始化配置
-- 该文件包含所有文件类型和角色的初始化配置

-- 使用INSERT IGNORE避免重复插入，忽略file_type, file_role冲突
INSERT IGNORE INTO file_definitions
(id, file_type, file_role, sheet_name, header_row, data_start_row, columns_json, enabled, created_at, updated_at)
VALUES
/* =======================
    CUSTOMS - source
    ======================= */
(
   UUID(),
   'CUSTOMS',
   'SOURCE',
   'Customs',
   1,
   2,
   '[{"col": "A", "header": "会员编号"}, {"col": "B", "header": "序号"}, {"col": "C", "header": "HAWB番号"}, {"col": "D", "header": "現地問合せ番号"}, {"col": "E", "header": "貨物個数"}, {"col": "F", "header": "貨物重量"}, {"col": "G", "header": "重量単位コード"}, {"col": "H", "header": "品名"}, {"col": "I", "header": "材质"}, {"col": "J", "header": "收件人名（删）"}, {"col": "K", "header": "輸入者名"}, {"col": "L", "header": "英文邮编录入(删)"}, {"col": "M", "header": "收件人地址(删)2"}, {"col": "N", "header": "輸入者住所（删）"}, {"col": "O", "header": "提取门牌(删)"}, {"col": "P", "header": "輸入者住所"}, {"col": "Q", "header": "輸入者 郵便番号"}, {"col": "R", "header": "輸入者電話番号"}, {"col": "S", "header": "輸出者名"}, {"col": "T", "header": "輸出者住所"}, {"col": "U", "header": "インボイス価格条件コード"}, {"col": "V", "header": "インボイス通貨コード"}, {"col": "W", "header": "インボイス価格"}, {"col": "X", "header": "单价（删）"}, {"col": "Y", "header": "運賃区分コード"}, {"col": "Z", "header": "運賃通貨コード"}, {"col": "AA", "header": "運賃"}, {"col": "AB", "header": "原産地コード"}, {"col": "AC", "header": "備考"}, {"col": "AD", "header": "收件人名（日文）"}, {"col": "AE", "header": "收件人地址"}, {"col": "AF", "header": "收件人电话"}, {"col": "AG", "header": "收件人邮编"}, {"col": "AH", "header": "依赖人名"}, {"col": "AI", "header": "依赖人地址"}, {"col": "AJ", "header": "依赖人电话"}, {"col": "AK", "header": "收件地址识别码"}, {"col": "AL", "header": "电商货识别码"}, {"col": "AM", "header": "电商平台码"}, {"col": "AN", "header": "电商平台名称"}, {"col": "AO", "header": ""}, {"col": "AP", "header": ""}, {"col": "AQ", "header": ""}, {"col": "AR", "header": ""}, {"col": "AS", "header": ""}, {"col": "AT", "header": ""}, {"col": "AU", "header": "单价（删）"}, {"col": "AV", "header": "发货地址（删）"}, {"col": "AW", "header": "发货省（删）"}, {"col": "AX", "header": "发货市（删）"}, {"col": "AY", "header": "收件人地址2（删）"}]',
   1,
   NOW(),
   NOW()
),

/* =======================
    CUSTOMS - output
    ======================= */
(
   UUID(),
   'CUSTOMS',
   'OUTPUT',
   'Customs',
   1,
   2,
   '[{"col": "A", "header": "会员编号"}, {"col": "B", "header": "序号"}, {"col": "C", "header": "HAWB番号"}, {"col": "D", "header": "現地問合せ番号"}, {"col": "E", "header": "貨物個数"}, {"col": "F", "header": "貨物重量"}, {"col": "G", "header": "重量単位コード"}, {"col": "H", "header": "品名"}, {"col": "I", "header": "材质"}, {"col": "J", "header": "輸入者名"}, {"col": "K", "header": "輸入者住所"}, {"col": "L", "header": "輸入者 郵便番号"}, {"col": "M", "header": "輸入者電話番号"}, {"col": "N", "header": "輸出者名"}, {"col": "O", "header": "輸出者住所"}, {"col": "P", "header": "インボイス価格条件コード"}, {"col": "Q", "header": "インボイス通貨コード"}, {"col": "R", "header": "インボイス価格"}, {"col": "S", "header": "運賃区分コード"}, {"col": "T", "header": "運賃通貨コード"}, {"col": "U", "header": "運賃"}, {"col": "V", "header": "原産地コード"}, {"col": "W", "header": "備考"}, {"col": "X", "header": "收件人名（日文）"}, {"col": "Y", "header": "收件人地址"}, {"col": "Z", "header": "收件人电话"}, {"col": "AA", "header": "收件人邮编"}, {"col": "AB", "header": "依赖人名"}, {"col": "AC", "header": "依赖人地址"}, {"col": "AD", "header": "依赖人电话"}, {"col": "AE", "header": "收件地址识别码"}, {"col": "AF", "header": "电商货识别码"}, {"col": "AG", "header": "电商平台码"}, {"col": "AH", "header": "电商平台名称"}, {"col": "AI", "header": ""}, {"col": "AJ", "header": ""}, {"col": "AK", "header": ""}, {"col": "AL", "header": ""}, {"col": "AM", "header": ""}, {"col": "AN", "header": ""}]',
   1,
   NOW(),
   NOW()
),

/* =======================
    DELIVERY - source
    ======================= */
(
   UUID(),
   'DELIVERY',
   'SOURCE',
   'Delivery',
   1,
   2,
   '[{"col": "A", "header": "お客様管理番号"}, {"col": "B", "header": "佐川問合せ番号HAWB"}, {"col": "C", "header": "配達指定日"}, {"col": "D", "header": "時間帯指定"}, {"col": "E", "header": "貨物個数"}, {"col": "F", "header": "お届け先人名"}, {"col": "G", "header": "お届け先住所"}, {"col": "H", "header": "お届け先電話"}, {"col": "I", "header": "お届け先郵便"}, {"col": "J", "header": "依頼主"}, {"col": "K", "header": "依頼主住所"}, {"col": "L", "header": "依頼主郵便番号"}, {"col": "M", "header": "依頼主電話"}, {"col": "N", "header": "佐川顧客コード（固定）"}, {"col": "O", "header": "記事欄2（品名）"}, {"col": "P", "header": "記事欄2"}, {"col": "Q", "header": "記事欄3"}, {"col": "R", "header": "收件人省州（删）"}, {"col": "S", "header": "收件人城市（删）"}, {"col": "T", "header": "收件人地址1（删）"}, {"col": "U", "header": "收件人地址2（删）"}, {"col": "V", "header": "発貨省（删）"}, {"col": "W", "header": "発貨市（删）"}, {"col": "X", "header": "発貨住所（删）"}]',
   1,
   NOW(),
   NOW()
),

/* =======================
    DELIVERY - output
    ======================= */
(
   UUID(),
   'DELIVERY',
   'OUTPUT',
   'Delivery',
   1,
   2,
   '[{"col": "A", "header": "お客様管理番号"}, {"col": "B", "header": "佐川問合せ番号HAWB"}, {"col": "C", "header": "配達指定日"}, {"col": "D", "header": "時間帯指定"}, {"col": "E", "header": "貨物個数"}, {"col": "F", "header": "お届け先人名"}, {"col": "G", "header": "お届け先住所"}, {"col": "H", "header": "お届け先電話"}, {"col": "I", "header": "お届け先郵便"}, {"col": "J", "header": "依頼主"}, {"col": "K", "header": "依頼主住所"}, {"col": "L", "header": "依頼主郵便番号"}, {"col": "M", "header": "依頼主電話"}, {"col": "N", "header": "佐川顧客コード（固定）"}, {"col": "O", "header": "記事欄2（品名）"}, {"col": "P", "header": "記事欄2"}, {"col": "Q", "header": "記事欄3"}]',
   1,
   NOW(),
   NOW()
);