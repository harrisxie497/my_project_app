import requests

# 测试登录接口
def test_login():
    print("测试登录接口...")
    url = "http://localhost:8000/api/v1/auth/login"
    data = {
        "username": "admin",
        "password": "admin123"
    }
    response = requests.post(url, data=data)
    print(f"登录响应状态码: {response.status_code}")
    print(f"登录响应内容: {response.json()}")
    
    if response.status_code == 200:
        return response.json()["data"]["access_token"]
    else:
        return None

# 测试获取当前用户信息
def test_me(token):
    print("\n测试获取当前用户信息接口...")
    url = "http://localhost:8000/api/v1/auth/me"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.get(url, headers=headers)
    print(f"获取用户信息响应状态码: {response.status_code}")
    print(f"获取用户信息响应内容: {response.json()}")

# 测试获取任务列表
def test_tasks(token):
    print("\n测试获取任务列表接口...")
    url = "http://localhost:8000/api/v1/tasks"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.get(url, headers=headers)
    print(f"获取任务列表响应状态码: {response.status_code}")
    print(f"获取任务列表响应内容: {response.json()}")

if __name__ == "__main__":
    token = test_login()
    if token:
        test_me(token)
        test_tasks(token)
