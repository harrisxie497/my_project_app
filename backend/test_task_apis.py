import requests
import json

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

def test_get_tasks(token):
    """测试获取任务列表"""
    print("\n=== 测试2: 获取任务列表 ===")
    url = f"{BASE_URL}/tasks"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.get(url, headers=headers)
    print(f"状态码: {response.status_code}")
    print(f"响应内容: {json.dumps(response.json(), ensure_ascii=False, indent=2)}")
    return response.status_code == 200

def test_create_task(token):
    """测试创建任务"""
    print("\n=== 测试3: 创建任务 ===")
    url = f"{BASE_URL}/tasks"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    # 准备测试数据
    data = {
        "file_type": "customs",
        "unique_code": "test_task_001",
        "flight_no": "NH123",
        "declare_date": "2026-01-22"
    }
    
    # 准备测试文件
    files = {
        "file": open("test_task_file.xlsx", "rb")
    }
    
    try:
        response = requests.post(url, data=data, files=files, headers=headers)
        print(f"状态码: {response.status_code}")
        print(f"响应内容: {json.dumps(response.json(), ensure_ascii=False, indent=2)}")
        
        if response.status_code == 200:
            task_id = response.json()["data"]["task_id"]
            print(f"任务创建成功，任务ID: {task_id}")
            return task_id
        return None
    except Exception as e:
        print(f"创建任务失败: {e}")
        return None
    finally:
        # 关闭文件
        files["file"].close()

def test_get_task_detail(token, task_id):
    """测试获取任务详情"""
    print(f"\n=== 测试4: 获取任务详情 (ID: {task_id}) ===")
    url = f"{BASE_URL}/tasks/{task_id}"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.get(url, headers=headers)
    print(f"状态码: {response.status_code}")
    print(f"响应内容: {json.dumps(response.json(), ensure_ascii=False, indent=2)}")
    return response.status_code == 200

def test_run_task(token, task_id):
    """测试运行任务"""
    print(f"\n=== 测试5: 运行任务 (ID: {task_id}) ===")
    url = f"{BASE_URL}/tasks/{task_id}/run"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.post(url, headers=headers)
    print(f"状态码: {response.status_code}")
    print(f"响应内容: {json.dumps(response.json(), ensure_ascii=False, indent=2)}")
    return response.status_code == 200

def test_download_task_file(token, task_id):
    """测试下载任务文件"""
    print(f"\n=== 测试6: 下载任务文件 (ID: {task_id}) ===")
    # 测试下载原始文件
    url = f"{BASE_URL}/tasks/{task_id}/files/original"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.get(url, headers=headers)
    print(f"状态码: {response.status_code}")
    if response.status_code == 200:
        print("成功获取原始文件")
        return True
    else:
        print(f"下载文件失败: {response.text}")
        return False

def main():
    """主测试函数"""
    print("开始测试任务相关API...")
    
    # 1. 登录获取token
    token = test_login()
    if not token:
        print("登录失败，无法继续测试")
        return
    
    # 2. 测试获取任务列表
    test_get_tasks(token)
    
    # 3. 测试创建任务
    task_id = test_create_task(token)
    if not task_id:
        print("创建任务失败，无法继续测试后续接口")
        return
    
    # 4. 测试获取任务详情
    test_get_task_detail(token, task_id)
    
    # 5. 测试运行任务
    test_run_task(token, task_id)
    
    # 6. 测试下载任务文件
    test_download_task_file(token, task_id)
    
    print("\n任务相关API测试完成！")

if __name__ == "__main__":
    main()