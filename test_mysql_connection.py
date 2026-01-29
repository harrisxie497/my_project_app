#!/usr/bin/env python3
# 测试MySQL连接
import pymysql

# MySQL连接参数
config = {
    'host': '172.18.207.224',
    'port': 3306,
    'user': 'app',
    'password': 'app123456',
    'database': 'demo',
    'charset': 'utf8mb4'
}

print("测试MySQL连接...")
print(f"连接参数: {config}")

# 测试连接
try:
    conn = pymysql.connect(**config)
    print("✅ MySQL连接成功！")
    
    # 测试查询
    with conn.cursor() as cursor:
        # 查询数据库版本
        cursor.execute("SELECT VERSION()")
        version = cursor.fetchone()[0]
        print(f"MySQL版本: {version}")
        
        # 查询用户表
        cursor.execute("SHOW TABLES LIKE 'user%'")
        tables = cursor.fetchall()
        print(f"用户相关表: {[table[0] for table in tables]}")
        
        # 如果有用户表，查询用户数量
        if any('user' in table[0] for table in tables):
            cursor.execute("SELECT COUNT(*) FROM user")
            user_count = cursor.fetchone()[0]
            print(f"用户数量: {user_count}")
            
    conn.close()
    print("✅ MySQL查询测试成功！")
    
except pymysql.err.OperationalError as e:
    print(f"❌ MySQL连接失败：{e}")
    print(f"错误代码: {e.args[0]}")
    print(f"错误信息: {e.args[1]}")
except Exception as e:
    print(f"❌ 其他错误：{e}")
