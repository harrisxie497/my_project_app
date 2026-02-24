import pymysql

def test_single_insert():
    connection = pymysql.connect(
        host='172.18.207.224',
        user='root',
        password='root123456',
        database='demo',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
    
    try:
        with connection.cursor() as cursor:
            sql = """
            INSERT INTO field_pipelines 
            (id, file_type, target_col, target_header, map_op, source_cols, field_type, rule_ref, rule_params_json, depends_on, `order`, enabled, created_at, updated_at) 
            VALUES 
            ('fp_test_001','CUSTOMS','A','会员编号','COPY','["A"]','COPY','[]',NULL,'[]',1,1,NOW(),NOW())
            """
            cursor.execute(sql)
            connection.commit()
            print("测试插入成功！")
            
    except Exception as e:
        print(f"测试插入失败: {e}")
        connection.rollback()
    finally:
        connection.close()

if __name__ == '__main__':
    test_single_insert()
