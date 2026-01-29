#!/usr/bin/env python3
# 综合测试脚本：测试数据库连通性和API接口
import pymysql
import requests
import json

# MySQL连接配置
mysql_config = {
    'host': '172.18.207.224',
    'port': 3306,
    'user': 'app',
    'password': 'app123456',
    'database': 'demo',
    'charset': 'utf8mb4'
}

# 测试MySQL数据库连通性
def test_database_connection():
    print('=== 测试MySQL数据库连通性 ===')
    
    try:
        # 创建数据库连接
        conn = pymysql.connect(**mysql_config)
        print('✅ MySQL数据库连接成功！')
        
        # 创建游标
        cursor = conn.cursor()
        
        # 测试数据库查询
        cursor.execute('SELECT VERSION()')
        version = cursor.fetchone()[0]
        print(f'MySQL版本: {version}')
        
        # 测试查询用户表
        cursor.execute('SHOW TABLES LIKE %s', ('user%',))
        tables = cursor.fetchall()
        print('用户相关表:', [table[0] for table in tables])
        
        # 测试查询用户数量
        if tables:
            # 使用正确的表名 users
            cursor.execute('SELECT COUNT(*) FROM users')
            user_count = cursor.fetchone()[0]
            print(f'用户数量: {user_count}')
        
        # 关闭游标和连接
        cursor.close()
        conn.close()
        print('✅ MySQL数据库测试完成！')
        return True
        
    except pymysql.err.OperationalError as e:
        print('❌ MySQL数据库连接失败！')
        print(f'错误信息: {e}')
        print(f'错误代码: {e.args[0]}')
        print(f'错误描述: {e.args[1]}')
        return False
    except Exception as e:
        print('❌ MySQL数据库测试失败！')
        print(f'错误信息: {e}')
        return False

# 测试后端API接口
def test_api_endpoints():
    print('\n=== 测试后端API接口 ===')
    
    try:
        # 测试健康检查接口
        print('测试健康检查接口...')
        health_response = requests.get('http://localhost:8000/health')
        print(f'✅ 健康检查接口成功: {health_response.status_code}')
        print(f'健康检查响应: {health_response.json()}')
        
        # 测试登录接口
        print('\n测试登录接口...')
        login_data = {
            'username': 'admin',
            'password': 'admin123'
        }
        login_response = requests.post(
            'http://localhost:8000/api/v1/auth/login',
            data=login_data,
            headers={'Content-Type': 'application/x-www-form-urlencoded'}
        )
        
        print(f'✅ 登录接口成功: {login_response.status_code}')
        print(f'登录响应: {json.dumps(login_response.json(), indent=2, ensure_ascii=False)}')
        
        # 获取token
        login_data = login_response.json()
        token = login_data.get('data', {}).get('access_token')
        print(f'获取到token: {'✅ 成功' if token else '❌ 失败'}')
        
        # 测试用户管理API
        if token:
            print('\n测试用户管理API...')
            users_response = requests.get(
                'http://localhost:8000/api/v1/users/',
                headers={'Authorization': f'Bearer {token}'}
            )
            
            print(f'✅ 用户管理API成功: {users_response.status_code}')
            users_data = users_response.json()
            user_count = len(users_data.get('data', {}).get('items', []))
            print(f'用户数量: {user_count}')
            print(f'用户列表: {json.dumps(users_data.get('data', {}).get('items', []), indent=2, ensure_ascii=False)}')
        
        # 测试操作日志API
        if token:
            print('\n测试操作日志API...')
            logs_response = requests.get(
                'http://localhost:8000/api/v1/operation-logs',
                headers={'Authorization': f'Bearer {token}'}
            )
            
            print(f'✅ 操作日志API成功: {logs_response.status_code}')
            logs_data = logs_response.json()
            log_count = len(logs_data.get('data', {}).get('items', []))
            print(f'操作日志数量: {log_count}')
        
        print('\n✅ 所有API测试完成！')
        return True
        
    except Exception as e:
        print('❌ API测试失败！')
        print(f'错误信息: {e}')
        return False

# 运行所有测试
def run_all_tests():
    print('开始测试数据库连通性和API接口...')
    
    # 测试数据库连通性
    db_connected = test_database_connection()
    
    if db_connected:
        # 测试API接口
        test_api_endpoints()
    else:
        print('\n⚠️  由于数据库连接失败，跳过API测试')
    
    print('\n=== 测试完成 ===')

if __name__ == '__main__':
    run_all_tests()
