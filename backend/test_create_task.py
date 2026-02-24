import requests
import json

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
        print(f"登录成功，Token: {token[:50]}...")
        return token
    else:
        print(f"登录失败: {response.text}")
        return None

def test_create_task(token):
    """测试创建任务"""
    print("\n=== 创建任务 ===")
    url = f"{BASE_URL}/tasks"
    headers = {"Authorization": f"Bearer {token}"}
    
    # 准备测试文件
    test_file_path = "test_data.xlsx"
    
    # 检查文件是否存在
    import os
    if not os.path.exists(test_file_path):
        print(f"测试文件不存在: {test_file_path}")
        return None
    
    # 准备表单数据
    files = {
        "file": open(test_file_path, "rb")
    }
    data = {
        "file_type": "customs",
        "unique_code": "test_001",
        "flight_no": "NH123",
        "declare_date": "2026-02-05",
        "header_params": json.dumps({"B1": "会员编号", "E1": "序号", "H1": "HAWB番号"})
    }
    
    try:
        response = requests.post(url, headers=headers, files=files, data=data)
        print(f"状态码: {response.status_code}")
        print(f"响应: {response.text}")
        
        if response.status_code == 200:
            result = response.json()
            task_id = result["data"]["task_id"]
            print(f"任务创建成功，任务ID: {task_id}")
            return task_id
        else:
            print(f"任务创建失败")
            return None
    finally:
        files["file"].close()

if __name__ == "__main__":
    # 登录
    token = test_login()
    
    if token:
        # 创建任务
        task_id = test_create_task(token)
        
        if task_id:
            print(f"\n测试完成！任务ID: {task_id}")
        else:
            print("\n任务创建失败")
