import requests
import json
import os

# 测试配置
BASE_URL = "http://localhost:8000/api/v1"
USERNAME = "admin"
PASSWORD = "admin123"

# 测试用xlsx文件路径（如果不存在则创建一个简单的）
TEST_FILE_PATH = "test_file.xlsx"

# 创建测试用xlsx文件（简单的Excel文件结构）
def create_test_xlsx():
    if not os.path.exists(TEST_FILE_PATH):
        # 创建一个简单的xlsx文件
        import openpyxl
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Sheet1"
        ws.append(["列1", "列2", "列3"])
        for i in range(10):
            ws.append([f"数据{i+1}", f"值{i+1}", f"内容{i+1}"])
        wb.save(TEST_FILE_PATH)
        print(f"创建了测试文件: {TEST_FILE_PATH}")
    else:
        print(f"使用现有的测试文件: {TEST_FILE_PATH}")

# 测试登录获取令牌
def test_login():
    print("=== 测试1: 登录获取JWT令牌 ===")
    url = f"{BASE_URL}/auth/login"
    data = {
        "username": USERNAME,
        "password": PASSWORD
    }
    response = requests.post(url, data=data)
    print(f"状态码: {response.status_code}")
    print(f"响应内容: {json.dumps(response.json(), ensure_ascii=False, indent=2)}")
    
    if response.status_code == 200:
        return response.json()["data"]["access_token"]
    else:
        return None

# 测试获取当前用户信息
def test_me(token):
    print("\n=== 测试2: 获取当前用户信息 ===")
    url = f"{BASE_URL}/auth/me"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.get(url, headers=headers)
    print(f"状态码: {response.status_code}")
    print(f"响应内容: {json.dumps(response.json(), ensure_ascii=False, indent=2)}")
    return response.status_code == 200

# 测试获取任务列表
def test_tasks(token):
    print("\n=== 测试3: 获取任务列表 ===")
    url = f"{BASE_URL}/tasks"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.get(url, headers=headers)
    print(f"状态码: {response.status_code}")
    print(f"响应内容: {json.dumps(response.json(), ensure_ascii=False, indent=2)}")
    return response.status_code == 200

# 测试创建任务（上传文件）
def test_create_task(token):
    print("\n=== 测试4: 创建任务（上传文件） ===")
    url = f"{BASE_URL}/tasks"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    files = {
        "file": open(TEST_FILE_PATH, "rb")
    }
    data = {
        "file_type": "customs",
        "unique_code": "TEST001",
        "flight_no": "NH123",
        "declare_date": "2026-01-20"
    }
    response = requests.post(url, headers=headers, files=files, data=data)
    print(f"状态码: {response.status_code}")
    print(f"响应内容: {json.dumps(response.json(), ensure_ascii=False, indent=2)}")
    
    if response.status_code == 200:
        return response.json()["data"]["task_id"]
    else:
        return None

# 测试获取任务详情
def test_get_task_detail(token, task_id):
    print(f"\n=== 测试5: 获取任务详情（任务ID: {task_id}） ===")
    url = f"{BASE_URL}/tasks/{task_id}"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.get(url, headers=headers)
    print(f"状态码: {response.status_code}")
    print(f"响应内容: {json.dumps(response.json(), ensure_ascii=False, indent=2)}")
    return response.status_code == 200

# 测试运行任务
def test_run_task(token, task_id):
    print(f"\n=== 测试6: 运行任务（任务ID: {task_id}） ===")
    url = f"{BASE_URL}/tasks/{task_id}/run"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.post(url, headers=headers)
    print(f"状态码: {response.status_code}")
    print(f"响应内容: {json.dumps(response.json(), ensure_ascii=False, indent=2)}")
    return response.status_code == 200

# 测试下载任务文件
def test_download_task_file(token, task_id):
    print(f"\n=== 测试7: 下载任务文件（任务ID: {task_id}） ===")
    url = f"{BASE_URL}/tasks/{task_id}/files/original"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.get(url, headers=headers)
    print(f"状态码: {response.status_code}")
    print(f"响应头: {dict(response.headers)}")
    
    if response.status_code == 200:
        # 保存下载的文件
        save_path = f"downloaded_original_{task_id}.xlsx"
        with open(save_path, "wb") as f:
            f.write(response.content)
        print(f"文件下载成功，保存为: {save_path}")
        return True
    else:
        return False

# 主测试函数
def run_all_tests():
    print("开始全面测试后端API...")
    print(f"测试环境: {BASE_URL}")
    print(f"测试用户: {USERNAME}")
    print("="*60)
    
    # 创建测试文件
    create_test_xlsx()
    
    # 测试结果记录
    results = []
    
    # 测试1: 登录获取令牌
    token = test_login()
    results.append("✓ 登录获取令牌" if token else "✗ 登录获取令牌")
    
    if token:
        # 测试2: 获取当前用户信息
        results.append("✓ 获取当前用户信息" if test_me(token) else "✗ 获取当前用户信息")
        
        # 测试3: 获取任务列表
        results.append("✓ 获取任务列表" if test_tasks(token) else "✗ 获取任务列表")
        
        # 测试4: 创建任务
        task_id = test_create_task(token)
        results.append("✓ 创建任务" if task_id else "✗ 创建任务")
        
        if task_id:
            # 测试5: 获取任务详情
            results.append("✓ 获取任务详情" if test_get_task_detail(token, task_id) else "✗ 获取任务详情")
            
            # 测试6: 运行任务
            results.append("✓ 运行任务" if test_run_task(token, task_id) else "✗ 运行任务")
            
            # 测试7: 下载任务文件
            results.append("✓ 下载任务文件" if test_download_task_file(token, task_id) else "✗ 下载任务文件")
        else:
            results.extend(["✗ 获取任务详情", "✗ 运行任务", "✗ 下载任务文件"])
    else:
        results.extend(["✗ 获取当前用户信息", "✗ 获取任务列表", "✗ 创建任务", 
                       "✗ 获取任务详情", "✗ 运行任务", "✗ 下载任务文件"])
    
    # 清理测试文件
    if os.path.exists(TEST_FILE_PATH):
        os.remove(TEST_FILE_PATH)
    
    # 输出测试结果汇总
    print("\n" + "="*60)
    print("测试结果汇总:")
    for result in results:
        print(f"  {result}")
    
    # 计算通过率
    passed = sum(1 for r in results if r.startswith("✓"))
    total = len(results)
    print(f"\n测试通过率: {passed}/{total} ({passed/total*100:.1f}%)")
    
    if passed == total:
        print("🎉 所有测试通过！")
        return True
    else:
        print("❌ 部分测试失败，请检查日志和代码")
        return False

if __name__ == "__main__":
    run_all_tests()
