import sqlite3
import os

# 检查SQLite数据库中的数据
def check_sqlite_data():
    # 获取当前目录
    current_dir = os.getcwd()
    print(f"当前工作目录: {current_dir}")
    
    # 检查数据库文件是否存在
    db_path = os.path.join(current_dir, 'backend', 'test.db')
    print(f"数据库文件路径: {db_path}")
    print(f"数据库文件是否存在: {os.path.exists(db_path)}")
    
    if not os.path.exists(db_path):
        print("数据库文件不存在")
        return
    
    # 连接到SQLite数据库
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # 获取所有表
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        print(f"\n数据库中的表: {[table[0] for table in tables]}")
        
        # 检查操作日志表
        if 'operation_logs' in [table[0] for table in tables]:
            print("\n=== 操作日志表数据 ===")
            cursor.execute("SELECT COUNT(*) FROM operation_logs;")
            count = cursor.fetchone()[0]
            print(f"操作日志总数: {count}")
            
            # 获取最新的5条操作日志
            cursor.execute("SELECT * FROM operation_logs ORDER BY created_at DESC LIMIT 5;")
            logs = cursor.fetchall()
            for log in logs:
                print(f"ID: {log[0]}, 用户ID: {log[1]}, 操作: {log[2]}, 成功: {log[5]}, 时间: {log[8]}")
        
        # 检查用户表
        if 'users' in [table[0] for table in tables]:
            print("\n=== 用户表数据 ===")
            cursor.execute("SELECT COUNT(*) FROM users;")
            count = cursor.fetchone()[0]
            print(f"用户总数: {count}")
            
            # 获取所有用户
            cursor.execute("SELECT * FROM users;")
            users = cursor.fetchall()
            for user in users:
                print(f"ID: {user[0]}, 用户名: {user[1]}, 角色: {user[4]}, 状态: {'启用' if user[5] else '禁用'}")
    
    except Exception as e:
        print(f"查询数据时出错: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    check_sqlite_data()
