import requests

BASE_URL = "http://127.0.0.1:8000/api/v1"

def test_login():
    """测试登录"""
    print("=== 登录 ===")
    url = f"{BASE_URL}/auth/login"
    data = {
        "username": "admin",
        "password": "123456"
    }
    response = requests.post(url, data=data)
    print(f"状态码: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        token = result["data"]["access_token"]
        print(f"登录成功")
        return token
    else:
        print(f"登录失败: {response.text}")
        return None

def test_field_pipelines(token):
    """测试字段映射配置接口"""
    print("\n=== 字段映射配置 ===")
    url = f"{BASE_URL}/field-pipelines"
    headers = {"Authorization": f"Bearer {token}"}
    
    response = requests.get(url, headers=headers)
    print(f"状态码: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"获取成功，数据数量: {len(result['data']['items'])}")
        print(f"第一条数据: {result['data']['items'][0]}")
    else:
        print(f"获取失败: {response.text}")

if __name__ == "__main__":
    # 登录
    token = test_login()
    
    if token:
        # 测试字段映射配置
        test_field_pipelines(token)
