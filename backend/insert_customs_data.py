import pymysql

conn = pymysql.connect(host='172.18.207.224', user='root', password='root123456', database='demo')
cursor = conn.cursor()

data = [
    ('CUSTOMS','A','会员编号','COPY','["A"]','COPY','[]',None,'[]',1,1,'NOW()','NOW()'),
    ('CUSTOMS','B','序号','NONE','[]','CALC','["seq_from_1"]',None,'[]',2,1,'NOW()','NOW()'),
    ('CUSTOMS','C','HAWB番号','COPY','["C"]','COPY','[]',None,'[]',3,1,'NOW()','NOW()'),
    ('CUSTOMS','D','現地問合せ番号','COPY','["D"]','COPY','[]',None,'[]',4,1,'NOW()','NOW()'),
    ('CUSTOMS','E','貨物個数','COPY','["E"]','COPY','[]',None,'[]',5,1,'NOW()','NOW()'),
    ('CUSTOMS','F','货物重量','NONE','["F","H","I"]','AI','["ai_weight_infer"]',None,'[]',6,1,'NOW()','NOW()'),
    ('CUSTOMS','G','重量单位代码','CONST','[]','CONST','["const_value"]','{"value":""}','[]',7,1,'NOW()','NOW()'),
    ('CUSTOMS','H','品名','NONE','["H"]','AI','["ai_goods_name_en"]',None,'[]',8,1,'NOW()','NOW()'),
    ('CUSTOMS','I','材质','NONE','["I"]','AI','["ai_material_translate_and_map"]',None,'[]',9,1,'NOW()','NOW()'),
    ('CUSTOMS','J','輸入者名','COPY','["K"]','COPY','[]',None,'[]',10,1,'NOW()','NOW()'),
    ('CUSTOMS','K','輸入者住所','COPY','["P"]','COPY','[]',None,'[]',11,1,'NOW()','NOW()'),
    ('CUSTOMS','L','輸入者 郵便番号','COPY','["Q"]','COPY','[]',None,'[]',12,1,'NOW()','NOW()'),
    ('CUSTOMS','M','輸入者電話番号','COPY','["R"]','COPY','[]',None,'[]',13,1,'NOW()','NOW()'),
    ('CUSTOMS','N','輸出者名','COPY','["S"]','COPY','[]',None,'[]',14,1,'NOW()','NOW()'),
    ('CUSTOMS','O','輸出者住所','COPY','["T"]','COPY','[]',None,'[]',15,1,'NOW()','NOW()'),
    ('CUSTOMS','P','インボイス价格条件代码','COPY','["U"]','COPY','[]',None,'[]',16,1,'NOW()','NOW()'),
    ('CUSTOMS','Q','インボイス通货代码','COPY','["V"]','COPY','[]',None,'[]',17,1,'NOW()','NOW()'),
    ('CUSTOMS','R','インボイス价格','COPY','["W"]','COPY','[]',None,'[]',18,1,'NOW()','NOW()'),
    ('CUSTOMS','S','运费区分代码','COPY','["Y"]','COPY','[]',None,'[]',19,1,'NOW()','NOW()'),
    ('CUSTOMS','T','运费通货代码','COPY','["Z"]','COPY','[]',None,'[]',20,1,'NOW()','NOW()'),
    ('CUSTOMS','U','运费','COPY','["AA"]','COPY','[]',None,'[]',21,1,'NOW()','NOW()'),
    ('CUSTOMS','V','原产地代码','COPY','["AB"]','COPY','[]',None,'[]',22,1,'NOW()','NOW()'),
    ('CUSTOMS','W','备注','COPY','["AC"]','FORMAT','["remove_brackets"]',None,'[]',23,1,'NOW()','NOW()'),
    ('CUSTOMS','X','收件人名（日文）','NONE','["AD"]','AI','["ai_receiver_name_clean_ja"]',None,'[]',24,1,'NOW()','NOW()'),
    ('CUSTOMS','Y','收件人地址','NONE','["AE","AY"]','AI','["ai_receiver_address_compose_ja"]',None,'[]',25,1,'NOW()','NOW()'),
    ('CUSTOMS','Z','收件人电话','COPY','["AF"]','COPY','[]',None,'[]',26,1,'NOW()','NOW()'),
    ('CUSTOMS','AA','收件人邮编','COPY','["AG"]','FORMAT','["remove_dash"]',None,'[]',27,1,'NOW()','NOW()'),
    ('CUSTOMS','AB','依赖人名','COPY','["AH"]','DEFAULT','["default_if_empty"]','{"default_value":"DIDA"}','[]',28,1,'NOW()','NOW()'),
    ('CUSTOMS','AC','依赖人地址','COPY','["AI"]','DEFAULT','["default_if_empty"]','{"default_value":"千葉県流山市平方8061GLPALFALINK81F13番シャッター"}','[]',29,1,'NOW()','NOW()'),
    ('CUSTOMS','AD','依赖人电话','COPY','["AJ"]','DEFAULT','["default_if_empty"]','{"default_value":"0471377848"}','[]',30,1,'NOW()','NOW()'),
    ('CUSTOMS','AE','收件地址识别码','COPY','["AK"]','COPY','[]',None,'[]',31,1,'NOW()','NOW()'),
    ('CUSTOMS','AF','电商货识别码','COPY','["AL"]','COPY','[]',None,'[]',32,1,'NOW()','NOW()'),
    ('CUSTOMS','AG','电商平台码','NONE','["AM"]','CALC','["lookup_platform_code_with_default"]',None,'[]',33,1,'NOW()','NOW()'),
    ('CUSTOMS','AH','电商平台名称','NONE','["AG"]','CALC','["map_platform_name_from_code_with_default"]','["AG"]',34,1,'NOW()','NOW()'),
    ('CUSTOMS','AI','系统预留列，不可使用','CONST','[]','CONST','["const_value"]','{"value":""}','[]',35,0,'NOW()','NOW()'),
    ('CUSTOMS','AJ','','CONST','[]','CONST','["const_value"]','{"value":""}','[]',36,0,'NOW()','NOW()'),
    ('CUSTOMS','AK','','CONST','[]','CONST','["const_value"]','{"value":""}','[]',37,0,'NOW()','NOW()'),
    ('CUSTOMS','AL','','CONST','[]','CONST','["const_value"]','{"value":""}','[]',38,0,'NOW()','NOW()'),
    ('CUSTOMS','AM','','CONST','[]','CONST','["const_value"]','{"value":""}','[]',39,0,'NOW()','NOW()'),
    ('CUSTOMS','AN','','CONST','[]','CONST','["const_value"]','{"value":""}','[]',40,0,'NOW()','NOW()'),
]

try:
    for row in data:
        sql = "INSERT INTO field_pipelines (file_type, target_col, target_header, map_op, source_cols, field_type, rule_ref, rule_params_json, depends_on, `order`, enabled, created_at, updated_at) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sql, row)
    conn.commit()
    print(f'成功插入{len(data)}条数据')
except Exception as e:
    print(f'插入失败: {e}')
    conn.rollback()
finally:
    conn.close()
