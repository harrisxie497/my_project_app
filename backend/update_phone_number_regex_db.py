"""
直接修改数据库中的电话号码配置
"""

import pymysql

def update_phone_number_regex():
    """更新电话号码的正则表达式"""
    print("=" * 100)
    print("更新电话号码的正则表达式")
    print("=" * 100)
    
    try:
        # 连接数据库
        connection = pymysql.connect(
            host='172.18.207.224',
            port=3306,
            user='app',
            password='app123456',
            database='demo',
            charset='utf8mb4'
        )
        
        cursor = connection.cursor()
        
        # 更新輸入者電話番号列的正则表达式
        sql1 = """
        UPDATE field_pipelines
        SET rule_params_json = JSON_SET(rule_params_json, '$.policy_copy_regex.regex', '^0\\\\d{9,11}$')
        WHERE target_header = '輸入者電話番号'
          AND file_type LIKE '%CUSTOMS%'
        """
        cursor.execute(sql1)
        print(f"✓ 更新輸入者電話番号列的正则表达式")
        
        # 更新收件人电话列的正则表达式
        sql2 = """
        UPDATE field_pipelines
        SET rule_params_json = JSON_SET(rule_params_json, '$.policy_copy_regex.regex', '^0\\\\d{9,11}$')
        WHERE target_header = '收件人电话'
          AND file_type LIKE '%CUSTOMS%'
        """
        cursor.execute(sql2)
        print(f"✓ 更新收件人电话列的正则表达式")
        
        # 提交更改
        connection.commit()
        print(f"\n✓ 更新成功！")
        
        # 验证更新
        print(f"\n验证更新结果：")
        sql3 = """
        SELECT target_header, rule_params_json
        FROM field_pipelines
        WHERE target_header IN ('輸入者電話番号', '收件人电话')
          AND file_type LIKE '%CUSTOMS%'
        """
        cursor.execute(sql3)
        results = cursor.fetchall()
        for row in results:
            print(f"  {row[0]}: {row[1]}")
        
        cursor.close()
        connection.close()
    
    except Exception as e:
        print(f"更新失败: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 100)
    print("更新完成")
    print("=" * 100)

if __name__ == "__main__":
    update_phone_number_regex()
