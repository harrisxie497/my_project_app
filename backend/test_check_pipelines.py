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

def test_get_field_pipelines(token):
    """测试获取字段映射配置"""
    print("\n=== 字段映射配置 ===")
    url = f"{BASE_URL}/field-pipelines"
    headers = {"Authorization": f"Bearer {token}"}
    
    response = requests.get(url, headers=headers)
    print(f"状态码: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        pipelines = result["data"]["items"]
        print(f"获取成功，数据数量: {len(pipelines)}")
        
        # 打印前5条配置的target_col
        for i, pipeline in enumerate(pipelines[:5]):
            print(f"  [{i+1}] target_col: {pipeline['target_col']}, source_cols: {pipeline['source_cols']}")
    else:
        print(f"获取失败: {response.text}")

if __name__ == "__main__":
    # 登录
    token = test_login()
    
    if token:
        # 测试字段映射配置
        test_get_field_pipelines(token)
