import pymysql

def check_users_table():
    """检查users表结构"""
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
        cursor.execute("DESCRIBE users")
        results = cursor.fetchall()
        
        print("users表结构：")
        for row in results:
            print(f"  字段名：{row[0]}, 类型：{row[1]}, 允许NULL：{row[2]}, 键：{row[3]}, 默认值：{row[4]}")
        
        # 查看所有用户
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        
        print("\nusers表中的所有用户：")
        for user in users:
            print(f"  {user}")
        
        cursor.close()
        connection.close()
        
    except Exception as e:
        print(f"查询失败：{str(e)}")

if __name__ == "__main__":
    check_users_table()
