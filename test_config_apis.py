import requests
import json

base_url = "http://localhost:8000/api/v1"

# 首先获取登录token
def get_auth_token():
    """
    获取认证token
    :return: str - 认证token
    """
    login_url = f"{base_url}/auth/login"
    login_data = {
        "username": "admin",
        "password": "admin123"
    }
    
    # 使用表单数据而不是JSON数据
    response = requests.post(login_url, data=login_data)
    if response.status_code == 200:
        data = response.json()
        if data.get("ok"):
            return data["data"]["access_token"]
    
    print(f"登录失败: {response.status_code} - {response.text}")
    return None

# 测试文件定义API
def test_file_definitions(token):
    """
    测试文件定义API
    :param token: str - 认证token
    """
    headers = {"Authorization": f"Bearer {token}"}
    
    # 测试获取文件定义列表
    print("\n=== 测试文件定义API ===")
    url = f"{base_url}/file-definitions"
    response = requests.get(url, headers=headers)
    print(f"获取文件定义列表: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"响应内容: {json.dumps(data, ensure_ascii=False, indent=2)}")
    else:
        print(f"请求失败: {response.text}")

# 测试字段映射API
def test_field_pipelines(token):
    """
    测试字段映射API
    :param token: str - 认证token
    """
    headers = {"Authorization": f"Bearer {token}"}
    
    # 测试获取字段映射列表
    print("\n=== 测试字段映射API ===")
    url = f"{base_url}/field-pipelines"
    response = requests.get(url, headers=headers)
    print(f"获取字段映射列表: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"响应内容: {json.dumps(data, ensure_ascii=False, indent=2)}")
    else:
        print(f"请求失败: {response.text}")

# 测试规则定义API
def test_rule_definitions(token):
    """
    测试规则定义API
    :param token: str - 认证token
    """
    headers = {"Authorization": f"Bearer {token}"}
    
    # 测试获取规则定义列表
    print("\n=== 测试规则定义API ===")
    url = f"{base_url}/rule-definitions"
    response = requests.get(url, headers=headers)
    print(f"获取规则定义列表: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"响应内容: {json.dumps(data, ensure_ascii=False, indent=2)}")
    else:
        print(f"请求失败: {response.text}")

if __name__ == "__main__":
    # 获取认证token
    token = get_auth_token()
    if token:
        print(f"获取到token: {token}")
        
        # 测试三个配置相关API
        test_file_definitions(token)
        test_field_pipelines(token)
        test_rule_definitions(token)
    else:
        print("无法获取认证token，测试终止")
