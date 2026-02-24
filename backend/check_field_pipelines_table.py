import pymysql

def check_field_pipelines_table():
    """检查field_pipelines表结构"""
    connection = pymysql.connect(
        host='172.18.207.224',
        user='root',
        password='root123456',
        database='demo',
        charset='utf8mb4'
    )
    
    try:
        cursor = connection.cursor()
        
        # 查看表结构
        cursor.execute("DESCRIBE field_pipelines")
        results = cursor.fetchall()
        
        print("field_pipelines表结构：")
        for row in results:
            print(f"  字段名：{row[0]}, 类型：{row[1]}, 允许NULL：{row[2]}, 键：{row[3]}, 默认值：{row[4]}")
        
        # 查看前几条数据
        cursor.execute("SELECT * FROM field_pipelines LIMIT 3")
        pipelines = cursor.fetchall()
        
        print("\nfield_pipelines表中的前3条数据：")
        for pipeline in pipelines:
            print(f"  {pipeline}")
        
        cursor.close()
        connection.close()
        
    except Exception as e:
        print(f"查询失败：{str(e)}")

if __name__ == "__main__":
    check_field_pipelines_table()
