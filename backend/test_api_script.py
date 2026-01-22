import requests
import json
import os
from openpyxl import Workbook

# 基础URL
BASE_URL = "http://localhost:8000/api/v1"

# 测试登录接口
def test_login():
    print("=== 测试登录接口 ===")
    url = f"{BASE_URL}/auth/login"
    data = {
        "username": "admin",
        "password": "admin123"
    }
    
    try:
        response = requests.post(url, data=data, headers={"Content-Type": "application/x-www-form-urlencoded"})
        print(f"状态码: {response.status_code}")
        print(f"响应内容: {response.text}")
        
        if response.status_code == 200:
            result = response.json()
            access_token = result.get("data", {}).get("access_token")
            if access_token:
                print(f"登录成功，获取到access_token: {access_token[:20]}...")
                return access_token
        
        return None
    except Exception as e:
        print(f"测试失败: {e}")
        return None

# 测试获取当前用户信息
def test_get_me(access_token):
    print("\n=== 测试获取当前用户信息接口 ===")
    url = f"{BASE_URL}/auth/me"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    
    try:
        response = requests.get(url, headers=headers)
        print(f"状态码: {response.status_code}")
        print(f"响应内容: {response.text}")
        return response.status_code == 200
    except Exception as e:
        print(f"测试失败: {e}")
        return False

# 测试获取任务列表
def test_get_tasks(access_token):
    print("\n=== 测试获取任务列表接口 ===")
    url = f"{BASE_URL}/tasks/"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    
    try:
        response = requests.get(url, headers=headers)
        print(f"状态码: {response.status_code}")
        print(f"响应内容: {response.text}")
        return response.status_code == 200
    except Exception as e:
        print(f"测试失败: {e}")
        return False

# 创建测试用的Excel文件
def create_test_excel():
    # 创建一个新的Excel工作簿
    wb = Workbook()
    ws = wb.active
    
    # 添加一些测试数据
    ws.append(["列1", "列2", "列3"])
    ws.append(["数据1", "数据2", "数据3"])
    ws.append(["数据4", "数据5", "数据6"])
    
    # 保存文件
    file_path = "test.xlsx"
    wb.save(file_path)
    print(f"已创建测试Excel文件: {file_path}")
    return file_path

# 测试文件上传接口
def test_upload_file(access_token, file_path):
    print("\n=== 测试文件上传接口 ===")
    url = f"{BASE_URL}/tasks/"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    
    # 准备表单数据
    data = {
        "file_type": "customs",
        "unique_code": "test_upload_001",
        "flight_no": "CA1234",
        "declare_date": "2026-01-21"
    }
    
    # 准备文件
    files = {
        "file": (os.path.basename(file_path), open(file_path, "rb"), "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    }
    
    try:
        response = requests.post(url, headers=headers, data=data, files=files)
        print(f"状态码: {response.status_code}")
        print(f"响应内容: {response.text}")
        
        if response.status_code == 200:
            result = response.json()
            task_id = result.get("data", {}).get("task_id")
            if task_id:
                print(f"文件上传成功，获取到任务ID: {task_id}")
                return task_id
        
        return None
    except Exception as e:
        print(f"测试失败: {e}")
        return None
    finally:
        # 关闭文件
        files["file"][1].close()

# 测试健康检查接口
def test_health_check():
    print("\n=== 测试健康检查接口 ===")
    url = "http://localhost:8000/health"
    
    try:
        response = requests.get(url)
        print(f"状态码: {response.status_code}")
        print(f"响应内容: {response.text}")
        return response.status_code == 200
    except Exception as e:
        print(f"测试失败: {e}")
        return False

# 测试运行任务接口
def test_run_task(access_token, task_id):
    print(f"\n=== 测试运行任务接口 ===")
    url = f"{BASE_URL}/tasks/{task_id}/run"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    
    try:
        response = requests.post(url, headers=headers)
        print(f"状态码: {response.status_code}")
        print(f"响应内容: {response.text}")
        return response.status_code == 200
    except Exception as e:
        print(f"测试失败: {e}")
        return False

# 测试获取任务详情接口
def test_get_task_detail(access_token, task_id):
    print(f"\n=== 测试获取任务详情接口 ===")
    url = f"{BASE_URL}/tasks/{task_id}"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    
    try:
        response = requests.get(url, headers=headers)
        print(f"状态码: {response.status_code}")
        print(f"响应内容: {response.text}")
        return response.status_code == 200
    except Exception as e:
        print(f"测试失败: {e}")
        return False

# 主函数
def main():
    print("开始测试后端接口...")
    
    # 测试登录
    access_token = test_login()
    
    if access_token:
        # 测试获取当前用户信息
        test_get_me(access_token)
        
        # 测试获取任务列表
        test_get_tasks(access_token)
        
        # 创建测试Excel文件
        test_file_path = create_test_excel()
        
        try:
            # 测试文件上传接口
            task_id = test_upload_file(access_token, test_file_path)
            
            if task_id:
                # 测试运行任务接口
                test_run_task(access_token, task_id)
                
                # 测试获取任务详情接口
                test_get_task_detail(access_token, task_id)
                
                # 再次测试获取任务列表，确认新任务已添加
                test_get_tasks(access_token)
        finally:
            # 删除测试文件
            if os.path.exists(test_file_path):
                os.remove(test_file_path)
                print(f"已删除测试Excel文件: {test_file_path}")
    
    # 测试健康检查接口
    test_health_check()
    
    print("\n后端接口测试完成!")

if __name__ == "__main__":
    main()
