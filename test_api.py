import requests
import json

# API基础URL
BASE_URL = "http://127.0.0.1:8000"

# 测试健康检查接口
def test_health_check():
    print("测试健康检查接口...")
    url = f"{BASE_URL}/health"
    response = requests.get(url)
    print(f"状态码: {response.status_code}")
    print(f"响应: {response.json()}")
    return response.status_code == 200

# 测试根路径接口
def test_root():
    print("\n测试根路径接口...")
    url = f"{BASE_URL}/"
    response = requests.get(url)
    print(f"状态码: {response.status_code}")
    print(f"响应: {response.json()}")
    return response.status_code == 200

# 测试API文档接口
def test_openapi():
    print("\n测试OpenAPI文档接口...")
    url = f"{BASE_URL}/openapi.json"
    response = requests.get(url)
    print(f"状态码: {response.status_code}")
    print(f"响应: 包含 {len(response.json().get('paths', {}))} 个路径")
    return response.status_code == 200

# 测试文件定义接口
def test_file_definitions():
    print("\n测试文件定义接口...")
    url = f"{BASE_URL}/api/v1/file-definitions/file-definitions/"
    response = requests.get(url)
    print(f"状态码: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"响应: 包含 {len(data.get('data', {}).get('items', []))} 个文件定义")
    return response.status_code == 200

# 测试字段映射接口
def test_field_pipelines():
    print("\n测试字段映射接口...")
    url = f"{BASE_URL}/api/v1/field-pipelines/field-pipelines/"
    response = requests.get(url)
    print(f"状态码: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"响应: 包含 {len(data.get('data', {}).get('items', []))} 个字段映射")
    return response.status_code == 200

# 测试规则定义接口
def test_rule_definitions():
    print("\n测试规则定义接口...")
    url = f"{BASE_URL}/api/v1/rule-definitions/rule-definitions/"
    response = requests.get(url)
    print(f"状态码: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"响应: 包含 {len(data.get('data', {}).get('items', []))} 个规则定义")
    return response.status_code == 200

# 测试认证登录接口
def test_auth_login():
    print("\n测试认证登录接口...")
    url = f"{BASE_URL}/api/v1/auth/login"
    payload = {
        "username": "admin",
        "password": "admin123"
    }
    headers = {
        "Content-Type": "application/json"
    }
    response = requests.post(url, json=payload, headers=headers)
    print(f"状态码: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"响应: 登录成功，返回token")
        return data.get("data", {}).get("access_token")
    else:
        print(f"响应: {response.json()}")
        return None

# 测试获取当前用户信息
def test_auth_me(token):
    print("\n测试获取当前用户信息接口...")
    url = f"{BASE_URL}/api/v1/auth/me"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.get(url, headers=headers)
    print(f"状态码: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"响应: 包含用户信息")
        return True
    else:
        print(f"响应: {response.json()}")
        return False

# 测试获取任务列表
def test_get_tasks():
    print("\n测试获取任务列表接口...")
    url = f"{BASE_URL}/api/v1/tasks"
    response = requests.get(url)
    print(f"状态码: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"响应: 包含 {len(data.get('data', {}).get('items', []))} 个任务")
    return response.status_code == 200

# 主函数
def main():
    print("开始测试API接口...\n")
    
    tests = [
        test_health_check,
        test_root,
        test_openapi,
        test_file_definitions,
        test_field_pipelines,
        test_rule_definitions,
        test_get_tasks
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        if test():
            passed += 1
        else:
            failed += 1
    
    # 测试需要认证的接口
    token = test_auth_login()
    if token:
        passed += 1
        if test_auth_me(token):
            passed += 1
        else:
            failed += 1
    else:
        failed += 1
        failed += 1
    
    print(f"\n测试完成！")
    print(f"通过: {passed}")
    print(f"失败: {failed}")
    print(f"成功率: {(passed / (passed + failed)) * 100:.2f}%")

if __name__ == "__main__":
    main()