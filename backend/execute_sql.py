import pymysql

conn = pymysql.connect(host='172.18.207.224', user='root', password='root123456', database='demo')
cursor = conn.cursor()

try:
    # 先删除CUSTOMS的field_pipelines数据
    cursor.execute('DELETE FROM field_pipelines WHERE file_type="CUSTOMS"')
    conn.commit()
    print(f'删除CUSTOMS数据: {cursor.rowcount}条')
    
    # 重新插入数据
    sql = open('init_customs_config.sql', 'r', encoding='utf-8').read()
    cursor.execute(sql)
    conn.commit()
    print(f'插入CUSTOMS数据: {cursor.rowcount}条')
    
except Exception as e:
    print(f'操作失败: {e}')
    conn.rollback()
finally:
    conn.close()
