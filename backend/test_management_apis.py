import requests
import json
from datetime import datetime

# 基础URL
BASE_URL = "http://localhost:8000/api/v1"

# 测试用户信息
USERNAME = "admin"
PASSWORD = "admin123"

def test_login():
    """测试登录并获取token"""
    print("=== 测试1: 登录获取JWT令牌 ===")
    url = f"{BASE_URL}/auth/login"
    data = {
        "username": USERNAME,
        "password": PASSWORD
    }
    response = requests.post(url, data=data, headers={"Content-Type": "application/x-www-form-urlencoded"})
    print(f"状态码: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"登录成功，获取到token")
        return result["data"]["access_token"]
    else:
        print(f"登录失败: {response.text}")
        return None

# 人员管理接口测试
def test_user_apis(token):
    """测试人员管理相关API"""
    print("\n=== 开始测试人员管理API ===")
    
    test_user_id = None
    test_username = "test_user_001"
    
    # 1. 获取用户列表
    print("\n1.1 获取用户列表")
    url = f"{BASE_URL}/users"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    print(f"状态码: {response.status_code}")
    print(f"响应内容: {json.dumps(response.json(), ensure_ascii=False, indent=2)}")
    
    # 2. 创建用户
    print("\n1.2 创建用户")
    url = f"{BASE_URL}/users"
    data = {
        "username": test_username,
        "display_name": "测试用户001",
        "password": "Test1234",
        "role": "operator"
    }
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    response = requests.post(url, json=data, headers=headers)
    print(f"状态码: {response.status_code}")
    print(f"响应内容: {json.dumps(response.json(), ensure_ascii=False, indent=2)}")
    
    if response.status_code == 200:
        test_user_id = response.json()["data"]["id"]
        print(f"创建用户成功，用户ID: {test_user_id}")
    
    # 3. 获取用户详情
    print(f"\n1.3 获取用户详情 (ID: {test_user_id})")
    url = f"{BASE_URL}/users/{test_user_id}"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    print(f"状态码: {response.status_code}")
    print(f"响应内容: {json.dumps(response.json(), ensure_ascii=False, indent=2)}")
    
    # 4. 更新用户信息
    print(f"\n1.4 更新用户信息 (ID: {test_user_id})")
    url = f"{BASE_URL}/users/{test_user_id}"
    data = {
        "display_name": "测试用户001更新",
        "role": "user"
    }
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    response = requests.put(url, json=data, headers=headers)
    print(f"状态码: {response.status_code}")
    print(f"响应内容: {json.dumps(response.json(), ensure_ascii=False, indent=2)}")
    
    # 5. 禁用用户
    print(f"\n1.5 禁用用户 (ID: {test_user_id})")
    url = f"{BASE_URL}/users/{test_user_id}/disable"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.put(url, headers=headers)
    print(f"状态码: {response.status_code}")
    print(f"响应内容: {json.dumps(response.json(), ensure_ascii=False, indent=2)}")
    
    # 6. 启用用户
    print(f"\n1.6 启用用户 (ID: {test_user_id})")
    url = f"{BASE_URL}/users/{test_user_id}/enable"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.put(url, headers=headers)
    print(f"状态码: {response.status_code}")
    print(f"响应内容: {json.dumps(response.json(), ensure_ascii=False, indent=2)}")
    
    # 7. 删除用户
    print(f"\n1.7 删除用户 (ID: {test_user_id})")
    url = f"{BASE_URL}/users/{test_user_id}"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.delete(url, headers=headers)
    print(f"状态码: {response.status_code}")
    print(f"响应内容: {json.dumps(response.json(), ensure_ascii=False, indent=2)}")
    
    # 8. 管理员获取用户列表
    print("\n1.8 管理员获取用户列表")
    url = f"{BASE_URL}/admin/users"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    print(f"状态码: {response.status_code}")
    print(f"响应内容: {json.dumps(response.json(), ensure_ascii=False, indent=2)}")

# 操作日志接口测试
def test_operation_log_apis(token):
    """测试操作日志相关API"""
    print("\n=== 开始测试操作日志API ===")
    
    # 1. 获取操作日志列表
    print("\n2.1 获取操作日志列表")
    url = f"{BASE_URL}/operation-logs"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    print(f"状态码: {response.status_code}")
    print(f"响应内容: {json.dumps(response.json(), ensure_ascii=False, indent=2)}")
    
    # 2. 按用户ID获取操作日志（使用admin用户ID）
    print("\n2.2 按用户ID获取操作日志")
    # 先获取admin用户ID
    url = f"{BASE_URL}/users"
    headers = {"Authorization": f"Bearer {token}"}
    user_response = requests.get(url, headers=headers)
    if user_response.status_code == 200:
        users = user_response.json()["data"]["items"]
        admin_user = next((u for u in users if u["username"] == "admin"), None)
        if admin_user:
            admin_user_id = admin_user["id"]
            print(f"使用admin用户ID: {admin_user_id} 测试")
            url = f"{BASE_URL}/operation-logs/user/{admin_user_id}"
            headers = {"Authorization": f"Bearer {token}"}
            response = requests.get(url, headers=headers)
            print(f"状态码: {response.status_code}")
            print(f"响应内容: {json.dumps(response.json(), ensure_ascii=False, indent=2)}")
    
    # 3. 按操作类型获取操作日志
    print("\n2.3 按操作类型获取操作日志")
    url = f"{BASE_URL}/operation-logs/action/login"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    print(f"状态码: {response.status_code}")
    print(f"响应内容: {json.dumps(response.json(), ensure_ascii=False, indent=2)}")
    
    # 4. 管理员查询操作日志
    print("\n2.4 管理员查询操作日志")
    url = f"{BASE_URL}/admin/operation-logs"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    print(f"状态码: {response.status_code}")
    print(f"响应内容: {json.dumps(response.json(), ensure_ascii=False, indent=2)}")

def main():
    """主测试函数"""
    print("开始测试管理相关API...")
    
    # 1. 登录获取token
    token = test_login()
    if not token:
        print("登录失败，无法继续测试")
        return
    
    # 2. 测试人员管理API
    test_user_apis(token)
    
    # 3. 测试操作日志API
    test_operation_log_apis(token)
    
    print("\n管理相关API测试完成！")

if __name__ == "__main__":
    main()