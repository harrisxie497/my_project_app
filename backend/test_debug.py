import requests
import json
import time
import os

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

def test_create_task(token):
    """测试创建任务"""
    print("\n=== 创建任务 ===")
    url = f"{BASE_URL}/tasks"
    headers = {"Authorization": f"Bearer {token}"}
    
    # 准备测试文件
    test_file_path = "test_data.xlsx"
    
    # 检查文件是否存在
    if not os.path.exists(test_file_path):
        print(f"测试文件不存在: {test_file_path}")
        return None
    
    # 准备表单数据
    files = {
        "file": open(test_file_path, "rb")
    }
    data = {
        "file_type": "customs",
        "unique_code": "test_debug_001",
        "flight_no": "NH789",
        "declare_date": "2026-02-05",
        "header_params": json.dumps({
            "mawb_no": "123-456789",
            "flight_no": "NH789",
            "arrival_date": "2026-02-05"
        })
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

def test_run_task(token, task_id):
    """测试运行任务"""
    print(f"\n=== 运行任务 ===")
    url = f"{BASE_URL}/tasks/{task_id}/run"
    headers = {"Authorization": f"Bearer {token}"}
    
    data = {
        "header_params": json.dumps({
            "mawb_no": "123-456789",
            "flight_no": "NH789",
            "arrival_date": "2026-02-05"
        })
    }
    
    response = requests.post(url, headers=headers, data=data)
    print(f"状态码: {response.status_code}")
    print(f"响应: {response.text}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"任务运行成功，任务ID: {result['data']['task_id']}, 状态: {result['data']['status']}")
        
        # 等待任务完成
        print("\n等待任务完成...")
        for i in range(10):
            time.sleep(2)
            task_status = test_get_task_status(token, task_id)
            print(f"  [{i+1}/10] 任务状态: {task_status}")
            
            if task_status in ["success", "failed"]:
                print(f"\n任务最终状态: {task_status}")
                break
    else:
        print(f"任务运行失败")

def test_get_task_status(token, task_id):
    """获取任务状态"""
    url = f"{BASE_URL}/tasks/{task_id}"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        result = response.json()
        return result["data"]["status"]
    return None

def test_download_result(token, task_id):
    """下载结果文件"""
    print(f"\n=== 下载结果文件 ===")
    url = f"{BASE_URL}/tasks/{task_id}/files/result"
    headers = {"Authorization": f"Bearer {token}"}
    
    response = requests.get(url, headers=headers)
    print(f"状态码: {response.status_code}")
    
    if response.status_code == 200:
        result_file = f"result_{task_id}.xlsx"
        with open(result_file, "wb") as f:
            f.write(response.content)
        print(f"结果文件下载成功: {result_file}")
        print(f"文件大小: {len(response.content)} bytes")
        return result_file
    else:
        print(f"下载失败")
        return None

def check_log_file():
    """检查日志文件"""
    print(f"\n=== 检查日志文件 ===")
    log_file = "logs/app.log"
    
    if os.path.exists(log_file):
        with open(log_file, "r", encoding="utf-8") as f:
            lines = f.readlines()
            print(f"日志文件总行数: {len(lines)}")
            print(f"\n最后50行日志:")
            print("=" * 100)
            for line in lines[-50:]:
                print(line.strip())
    else:
        print(f"日志文件不存在: {log_file}")

if __name__ == "__main__":
    # 登录
    token = test_login()
    
    if token:
        # 创建新任务
        task_id = test_create_task(token)
        
        if task_id:
            # 运行任务
            test_run_task(token, task_id)
            
            # 下载结果
            test_download_result(token, task_id)
            
            # 检查日志
            check_log_file()
        else:
            print("\n任务创建失败")
    else:
        print("\n登录失败")
