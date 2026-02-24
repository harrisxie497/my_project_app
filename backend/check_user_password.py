import pymysql

def check_user_password():
    """检查数据库中的用户密码"""
    connection = pymysql.connect(
        host='172.18.207.224',
        user='root',
        password='root123456',
        database='demo',
        charset='utf8mb4'
    )
    
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT username, password FROM users")
        results = cursor.fetchall()
        
        print("数据库中的用户列表：")
        for row in results:
            username, hashed_password = row
            print(f"  用户名：{username}")
            print(f"  哈希密码：{hashed_password}")
        
        cursor.close()
        connection.close()
        
    except Exception as e:
        print(f"查询失败：{str(e)}")

if __name__ == "__main__":
    check_user_password()
