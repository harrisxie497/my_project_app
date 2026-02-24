import pymysql

def add_header_params_field():
    """为tasks表添加header_params字段"""
    connection = pymysql.connect(
        host='172.18.207.224',
        user='root',
        password='root123456',
        database='demo',
        charset='utf8mb4'
    )
    
    try:
        cursor = connection.cursor()
        
        # 检查字段是否已存在
        cursor.execute("SHOW COLUMNS FROM tasks LIKE 'header_params'")
        result = cursor.fetchone()
        
        if result:
            print("header_params字段已存在，无需添加")
        else:
            # 添加字段
            sql = "ALTER TABLE tasks ADD COLUMN header_params VARCHAR(1000) NULL COMMENT '表头参数JSON字符串'"
            cursor.execute(sql)
            print("成功添加header_params字段到tasks表")
        
        connection.commit()
        cursor.close()
        connection.close()
        
    except Exception as e:
        print(f"操作失败：{str(e)}")
        connection.rollback()

if __name__ == "__main__":
    add_header_params_field()
