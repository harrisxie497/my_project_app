import requests
import json

BASE_URL = "http://127.0.0.1:8000/api/v1"

def test_login(username, password):
    """测试登录接口"""
    print(f"\n=== 测试登录接口 - 用户名: {username} ===")
    url = f"{BASE_URL}/auth/login"
    data = {
        "username": username,
        "password": password
    }
    response = requests.post(url, data=data)
    print(f"状态码: {response.status_code}")
    print(f"响应: {response.text}")
    if response.status_code == 200:
        result = response.json()
        token = result["data"]["access_token"]
        print(f"获取Token成功: {token[:50]}...")
        return token
    else:
        print("登录失败")
        return None

def test_get_me(token):
    """测试获取当前用户信息接口"""
    print("\n=== 测试获取当前用户信息接口 ===")
    url = f"{BASE_URL}/auth/me"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    print(f"状态码: {response.status_code}")
    print(f"响应: {response.text}")

def test_get_tasks(token):
    """测试获取任务列表接口"""
    print("\n=== 测试获取任务列表接口 ===")
    url = f"{BASE_URL}/tasks"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    print(f"状态码: {response.status_code}")
    print(f"响应: {response.text}")

def test_health_check():
    """测试健康检查接口"""
    print("\n=== 测试健康检查接口 ===")
    url = "http://127.0.0.1:8000/health"
    response = requests.get(url)
    print(f"状态码: {response.status_code}")
    print(f"响应: {response.text}")

def test_root():
    """测试根路径接口"""
    print("\n=== 测试根路径接口 ===")
    url = "http://127.0.0.1:8000/"
    response = requests.get(url)
    print(f"状态码: {response.status_code}")
    print(f"响应: {response.text}")

if __name__ == "__main__":
    print("开始测试后端接口...")
    
    # 测试健康检查
    test_health_check()
    
    # 测试根路径
    test_root()
    
    # 尝试不同的用户登录
    test_users = [
        ("admin", "admin123"),
        ("admin", "123456"),
        ("harris", "harris"),
        ("rop", "rop"),
    ]
    
    token = None
    for username, password in test_users:
        token = test_login(username, password)
        if token:
            break
    
    if token:
        # 测试获取用户信息
        test_get_me(token)
        
        # 测试获取任务列表
        test_get_tasks(token)
    else:
        print("\n所有登录尝试都失败了")
    
    print("\n=== 所有接口测试完成 ===")
