import pymysql

conn = pymysql.connect(
    host='172.18.207.224',
    user='root',
    password='root123456',
    database='demo'
)

try:
    with conn.cursor() as cursor:
        # 1. 插入field_pipelines配置（清关文件字段映射）
        # 启用的字段
        enabled_fields = [
            ('CUSTOMS', 'A', '会员编号', 'COPY', '["会员编号"]', 'TEXT', '[]', '[]', 1, True),
            ('CUSTOMS', 'B', '序号', 'NONE', '[]', 'NUMBER', '["seq_from_1"]', '[]', 2, True),
            ('CUSTOMS', 'C', 'HAWB番号', 'COPY', '["HAWB番号"]', 'TEXT', '[]', '[]', 3, True),
            ('CUSTOMS', 'D', '現地問合せ番号', 'COPY', '["現地問合せ番号"]', 'TEXT', '[]', '[]', 4, True),
            ('CUSTOMS', 'E', '貨物個数', 'COPY', '["貨物個数"]', 'NUMBER', '[]', '[]', 5, True),
            ('CUSTOMS', 'F', '貨物重量', 'NONE', '["貨物重量"]', 'NUMBER', '["ai_weight_infer"]', '[]', 6, True),
            ('CUSTOMS', 'G', '重量単位コード', 'CONST', '[]', 'TEXT', '["const_value"]', '[]', 7, True),
            ('CUSTOMS', 'H', '品名', 'NONE', '["品名"]', 'TEXT', '["ai_goods_name_en"]', '[]', 8, True),
            ('CUSTOMS', 'I', '材质', 'NONE', '["材质"]', 'TEXT', '["ai_material_translate_and_map"]', '[]', 9, True),
            ('CUSTOMS', 'J', '輸入者名', 'COPY', '["輸入者名"]', 'TEXT', '[]', '[]', 10, True),
            ('CUSTOMS', 'K', '輸入者住所', 'COPY', '["輸入者住所"]', 'TEXT', '[]', '[]', 11, True),
            ('CUSTOMS', 'L', '輸入者 郵便番号', 'COPY', '["輸入者 郵便番号"]', 'TEXT', '[]', '[]', 12, True),
            ('CUSTOMS', 'M', '輸入者電話番号', 'COPY', '["輸入者電話番号"]', 'TEXT', '[]', '[]', 13, True),
            ('CUSTOMS', 'N', '輸出者名', 'COPY', '["輸出者名"]', 'TEXT', '[]', '[]', 14, True),
            ('CUSTOMS', 'O', '輸出者住所', 'COPY', '["輸出者住所"]', 'TEXT', '[]', '[]', 15, True),
            ('CUSTOMS', 'P', 'インボイス価格条件コード', 'COPY', '["インボイス価格条件コード"]', 'TEXT', '[]', '[]', 16, True),
            ('CUSTOMS', 'Q', 'インボイス通貨コード', 'COPY', '["インボイス通貨コード"]', 'TEXT', '[]', '[]', 17, True),
            ('CUSTOMS', 'R', 'インボイス価格', 'COPY', '["インボイス価格"]', 'NUMBER', '[]', '[]', 18, True),
            ('CUSTOMS', 'S', '運賃区分コード', 'COPY', '["運賃区分コード"]', 'TEXT', '[]', '[]', 19, True),
            ('CUSTOMS', 'T', '運賃通貨コード', 'COPY', '["運賃通貨コード"]', 'TEXT', '[]', '[]', 20, True),
            ('CUSTOMS', 'U', '運賃', 'COPY', '["運賃"]', 'NUMBER', '[]', '[]', 21, True),
            ('CUSTOMS', 'V', '原産地コード', 'COPY', '["原産地コード"]', 'TEXT', '[]', '[]', 22, True),
            ('CUSTOMS', 'W', '備考', 'COPY', '["備考"]', 'TEXT', '[]', '[]', 23, True),
            ('CUSTOMS', 'X', '收件人名（日文）', 'COPY', '["收件人名（日文）"]', 'TEXT', '[]', '[]', 24, True),
            ('CUSTOMS', 'Y', '收件人地址', 'COPY', '["收件人地址"]', 'TEXT', '[]', '[]', 25, True),
            ('CUSTOMS', 'Z', '收件人电话', 'COPY', '["收件人电话"]', 'TEXT', '[]', '[]', 26, True),
            ('CUSTOMS', 'AA', '收件人邮编', 'COPY', '["收件人邮编"]', 'TEXT', '[]', '[]', 27, True),
            ('CUSTOMS', 'AB', '依赖人名', 'COPY', '["依赖人名"]', 'TEXT', '[]', '[]', 28, True),
            ('CUSTOMS', 'AC', '依赖人地址', 'COPY', '["依赖人地址"]', 'TEXT', '[]', '[]', 29, True),
            ('CUSTOMS', 'AD', '依赖人电话', 'COPY', '["依赖人电话"]', 'TEXT', '[]', '[]', 30, True),
            ('CUSTOMS', 'AE', '收件地址识别码', 'COPY', '["收件地址识别码"]', 'TEXT', '[]', '[]', 31, True),
            ('CUSTOMS', 'AF', '电商货识别码', 'COPY', '["电商货识别码"]', 'TEXT', '[]', '[]', 32, True),
            ('CUSTOMS', 'AH', '电商平台码', 'COPY', '["电商平台码"]', 'TEXT', '[]', '[]', 33, True),
            ('CUSTOMS', 'AN', '电商平台名称', 'COPY', '["电商平台名称"]', 'TEXT', '[]', '[]', 34, True),
        ]

        # 禁用的字段
        disabled_fields = [
            ('CUSTOMS', 'J', '收件人名（删）', 'COPY', '["收件人名（删）"]', 'TEXT', '[]', '[]', 35, False),
            ('CUSTOMS', 'L', '英文邮编录入(删)', 'COPY', '["英文邮编录入(删)"]', 'TEXT', '[]', '[]', 36, False),
            ('CUSTOMS', 'M', '收件人地址(删)2', 'COPY', '["收件人地址(删)2"]', 'TEXT', '[]', '[]', 37, False),
            ('CUSTOMS', 'N', '輸入者住所（删）', 'COPY', '["輸入者住所（删）"]', 'TEXT', '[]', '[]', 38, False),
            ('CUSTOMS', 'O', '提取门牌(删)', 'COPY', '["提取门牌(删)"]', 'TEXT', '[]', '[]', 39, False),
            ('CUSTOMS', 'X', '单价（删）', 'COPY', '["单价（删）"]', 'NUMBER', '[]', '[]', 40, False),
            ('CUSTOMS', 'AP', '收件人省州（删）', 'COPY', '["收件人省州（删）"]', 'TEXT', '[]', '[]', 41, False),
            ('CUSTOMS', 'AQ', '收件人城市（删）', 'COPY', '["收件人城市（删）"]', 'TEXT', '[]', '[]', 42, False),
            ('CUSTOMS', 'AR', '收件人地址（删）', 'COPY', '["收件人地址（删）"]', 'TEXT', '[]', '[]', 43, False),
            ('CUSTOMS', 'AS', '申报品名（删）', 'COPY', '["申报品名（删）"]', 'TEXT', '[]', '[]', 44, False),
            ('CUSTOMS', 'AT', '材质(删)', 'COPY', '["材质(删)"]', 'TEXT', '[]', '[]', 45, False),
            ('CUSTOMS', 'AU', '单价（删）', 'COPY', '["单价（删）"]', 'NUMBER', '[]', '[]', 46, False),
            ('CUSTOMS', 'AV', '发货地址（删）', 'COPY', '["发货地址（删）"]', 'TEXT', '[]', '[]', 47, False),
            ('CUSTOMS', 'AW', '发货省（删）', 'COPY', '["发货省（删）"]', 'TEXT', '[]', '[]', 48, False),
            ('CUSTOMS', 'AX', '发货市（删）', 'COPY', '["发货市（删）"]', 'TEXT', '[]', '[]', 49, False),
            ('CUSTOMS', 'AY', '收件人地址2（删）', 'COPY', '["收件人地址2（删）"]', 'TEXT', '[]', '[]', 50, False),
        ]

        # 插入启用字段
        for f in enabled_fields:
            sql = """
                INSERT IGNORE INTO field_pipelines
                (id, file_type, target_col, target_header, map_op, source_cols, field_type, rule_ref, depends_on, `order`, enabled, created_at, updated_at)
                VALUES (UUID(), %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW(), NOW())
            """
            cursor.execute(sql, f)

        # 插入禁用字段
        for f in disabled_fields:
            sql = """
                INSERT IGNORE INTO field_pipelines
                (id, file_type, target_col, target_header, map_op, source_cols, field_type, rule_ref, depends_on, `order`, enabled, created_at, updated_at)
                VALUES (UUID(), %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW(), NOW())
            """
            cursor.execute(sql, f)

        conn.commit()

        # 检查结果
        cursor.execute('SELECT COUNT(*) FROM field_pipelines WHERE file_type = "CUSTOMS"')
        customs_count = cursor.fetchone()[0]
        print(f'清关字段映射记录数: {customs_count}')

        cursor.execute('SELECT COUNT(*) FROM field_pipelines WHERE file_type = "CUSTOMS" AND enabled = 1')
        enabled_count = cursor.fetchone()[0]
        print(f'启用字段数: {enabled_count}')
        cursor.execute('SELECT COUNT(*) FROM field_pipelines WHERE file_type = "CUSTOMS" AND enabled = 0')
        disabled_count = cursor.fetchone()[0]
        print(f'禁用字段数: {disabled_count}')

        # 查看前5个启用字段
        cursor.execute('SELECT target_col, target_header FROM field_pipelines WHERE file_type = "CUSTOMS" AND enabled = 1 ORDER BY `order` LIMIT 5')
        records = cursor.fetchall()
        print('前5个启用字段:')
        for record in records:
            print(f'  - {record[0]}: {record[1]}')

finally:
    conn.close()
