import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder
import os
import json
from datetime import datetime

# 测试配置
BASE_URL = "http://localhost:8000/api/v1"
TEST_USERNAME = "admin"
TEST_PASSWORD = "admin123"

# 测试结果记录
results = {
    "total": 0,
    "passed": 0,
    "failed": 0,
    "errors": []
}

# 辅助函数：打印测试结果
def print_test_result(name, status, message=""):
    results["total"] += 1
    if status == "PASSED":
        results["passed"] += 1
        print(f"✓ {name}: PASSED")
    else:
        results["failed"] += 1
        error_msg = f"✗ {name}: FAILED - {message}"
        print(error_msg)
        results["errors"].append(error_msg)

# 辅助函数：执行GET请求
def test_get_request(name, url, token, expected_status=200):
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == expected_status:
            print_test_result(name, "PASSED")
            return response.json()
        else:
            print_test_result(name, "FAILED", f"Status code {response.status_code} != {expected_status}")
            return None
    except Exception as e:
        print_test_result(name, "FAILED", str(e))
        return None

# 辅助函数：执行POST请求
def test_post_request(name, url, token, data=None, json_data=None, files=None, expected_status=200):
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    try:
        response = requests.post(url, headers=headers, data=data, json=json_data, files=files, timeout=10)
        if response.status_code == expected_status:
            print_test_result(name, "PASSED")
            return response.json()
        else:
            print_test_result(name, "FAILED", f"Status code {response.status_code} != {expected_status}: {response.text}")
            return None
    except Exception as e:
        print_test_result(name, "FAILED", str(e))
        return None

# 辅助函数：执行PUT请求
def test_put_request(name, url, token, data=None, json_data=None, expected_status=200):
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    try:
        response = requests.put(url, headers=headers, data=data, json=json_data, timeout=10)
        if response.status_code == expected_status:
            print_test_result(name, "PASSED")
            return response.json()
        else:
            print_test_result(name, "FAILED", f"Status code {response.status_code} != {expected_status}: {response.text}")
            return None
    except Exception as e:
        print_test_result(name, "FAILED", str(e))
        return None

# 辅助函数：执行DELETE请求
def test_delete_request(name, url, token, expected_status=200):
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    try:
        response = requests.delete(url, headers=headers, timeout=10)
        if response.status_code == expected_status:
            print_test_result(name, "PASSED")
            return response.json()
        else:
            print_test_result(name, "FAILED", f"Status code {response.status_code} != {expected_status}: {response.text}")
            return None
    except Exception as e:
        print_test_result(name, "FAILED", str(e))
        return None

# 1. 测试登录接口
def test_login():
    print("\n=== 测试认证相关接口 ===")
    url = f"{BASE_URL}/auth/login"
    data = {
        "username": TEST_USERNAME,
        "password": TEST_PASSWORD
    }
    response = test_post_request("登录接口", url, None, data=data)
    if response and response.get("ok"):
        return response["data"]["access_token"]
    return None

# 2. 测试获取当前用户信息
def test_me(token):
    url = f"{BASE_URL}/auth/me"
    return test_get_request("获取当前用户信息", url, token)

# 3. 测试任务管理API
def test_tasks(token):
    print("\n=== 测试任务管理API ===")
    # 测试获取任务列表
    test_get_request("获取任务列表", f"{BASE_URL}/tasks", token)

# 4. 测试规则表管理API
def test_rule_tables(token):
    print("\n=== 测试规则表管理API ===")
    # 测试获取规则表列表
    test_get_request("获取规则表列表", f"{BASE_URL}/rule-tables", token)
    
    # 测试获取规则表列表（管理员接口）
    test_get_request("获取规则表列表（管理员）", f"{BASE_URL}/admin/rule-tables", token)

# 5. 测试规则项管理API
def test_rule_items(token):
    print("\n=== 测试规则项管理API ===")
    # 测试获取规则项列表
    test_get_request("获取规则项列表", f"{BASE_URL}/rule-items", token)
    
    # 测试规则导入接口（文件上传）
    # 注意：这里需要一个实际的Excel文件进行测试
    # 我们先创建一个简单的测试文件
    test_file_path = "test_rules.xlsx"
    # 创建一个空的Excel文件（实际测试时需要替换为真实的测试文件）
    with open(test_file_path, "w") as f:
        f.write("PK\x03\x04")  # 简单的ZIP文件头，模拟空Excel文件
    
    try:
        # 使用multipart/form-data上传文件
        url = f"{BASE_URL}/admin/rules/import"
        with open(test_file_path, "rb") as f:
            files = {"file": (test_file_path, f, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")}
            response = requests.post(url, headers={"Authorization": f"Bearer {token}"}, files=files, timeout=10)
            if response.status_code == 400:  # 预期会失败，因为文件是假的
                print_test_result("规则导入接口（文件上传）", "PASSED", "预期失败，因为文件格式不正确")
            else:
                print_test_result("规则导入接口（文件上传）", "FAILED", f"预期状态码400，实际得到{response.status_code}")
    except Exception as e:
        print_test_result("规则导入接口（文件上传）", "FAILED", str(e))
    finally:
        # 清理测试文件
        if os.path.exists(test_file_path):
            os.remove(test_file_path)

# 6. 测试模板映射管理API
def test_template_mappings(token):
    print("\n=== 测试模板映射管理API ===")
    # 测试获取模板映射列表
    test_get_request("获取模板映射列表", f"{BASE_URL}/template-mappings", token)
    
    # 测试获取模板映射列表（管理员接口）
    test_get_request("获取模板映射列表（管理员）", f"{BASE_URL}/admin/template-mappings", token)

# 7. 测试AI字段能力管理API
def test_ai_capabilities(token):
    print("\n=== 测试AI字段能力管理API ===")
    # 测试获取AI字段能力列表
    test_get_request("获取AI字段能力列表", f"{BASE_URL}/ai-capabilities", token)
    
    # 测试获取AI字段能力列表（管理员接口）
    test_get_request("获取AI字段能力列表（管理员）", f"{BASE_URL}/admin/ai-capabilities", token)

# 8. 测试Excel配置管理API
def test_excel_configs(token):
    print("\n=== 测试Excel配置管理API ===")
    # 测试获取Excel配置列表
    test_get_request("获取Excel配置列表", f"{BASE_URL}/excel-configs", token)
    
    # 测试获取当前Excel配置（管理员接口）
    test_get_request("获取当前Excel配置（管理员）", f"{BASE_URL}/admin/excel-configs/active?file_type=customs", token)

# 9. 测试用户管理API
def test_users(token):
    print("\n=== 测试用户管理API ===")
    # 测试获取用户列表
    test_get_request("获取用户列表", f"{BASE_URL}/users", token)
    
    # 测试获取用户列表（管理员接口）
    test_get_request("获取用户列表（管理员）", f"{BASE_URL}/admin/users", token)

# 10. 测试操作日志API
def test_operation_logs(token):
    print("\n=== 测试操作日志API ===")
    # 测试获取操作日志列表
    test_get_request("获取操作日志列表", f"{BASE_URL}/operation-logs", token)
    
    # 测试获取操作日志列表（管理员接口）
    test_get_request("获取操作日志列表（管理员）", f"{BASE_URL}/admin/operation-logs", token)

# 主测试函数
def run_all_tests():
    print("开始执行API测试...")
    print(f"测试目标: {BASE_URL}")
    print(f"测试用户: {TEST_USERNAME}")
    print("=" * 50)
    
    # 1. 登录获取令牌
    token = test_login()
    if not token:
        print("\n❌ 登录失败，无法继续测试")
        return
    
    # 2. 执行其他测试
    test_me(token)
    test_tasks(token)
    test_rule_tables(token)
    test_rule_items(token)
    test_template_mappings(token)
    test_ai_capabilities(token)
    test_excel_configs(token)
    test_users(token)
    test_operation_logs(token)
    
    # 3. 打印测试总结
    print("\n" + "=" * 50)
    print("测试总结：")
    print(f"总测试数: {results['total']}")
    print(f"通过数: {results['passed']}")
    print(f"失败数: {results['failed']}")
    
    if results['errors']:
        print("\n错误详情：")
        for error in results['errors']:
            print(f"  - {error}")
    
    # 4. 生成测试报告
    generate_test_report()
    
    print("\n测试完成！")

# 生成测试报告
def generate_test_report():
    report = {
        "test_date": datetime.now().isoformat(),
        "base_url": BASE_URL,
        "test_user": TEST_USERNAME,
        "results": results,
        "errors": results["errors"]
    }
    
    # 保存JSON报告
    with open("api_test_report.json", "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    # 生成HTML报告
    html_report = f"""
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>API测试报告</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; }}
            .header {{ background: #f0f0f0; padding: 10px; border-radius: 5px; margin-bottom: 20px; }}
            .summary {{ margin: 20px 0; }}
            .status {{ font-weight: bold; }}
            .passed {{ color: green; }}
            .failed {{ color: red; }}
            .error-list {{ margin-top: 20px; }}
            .error-item {{ background: #ffebee; padding: 10px; margin: 5px 0; border-radius: 3px; }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>API测试报告</h1>
            <p>测试时间: {report['test_date']}</p>
            <p>测试目标: {report['base_url']}</p>
            <p>测试用户: {report['test_user']}</p>
        </div>
        
        <div class="summary">
            <h2>测试结果摘要</h2>
            <p>总测试数: <span class="status">{report['results']['total']}</span></p>
            <p>通过数: <span class="status passed">{report['results']['passed']}</span></p>
            <p>失败数: <span class="status failed">{report['results']['failed']}</span></p>
        </div>
        
        <div class="error-list">
            <h2>错误详情</h2>
            {''.join([f'<div class="error-item">{error}</div>' for error in report['errors']]) if report['errors'] else '<p>没有错误</p>'}
        </div>
    </body>
    </html>
    """
    
    with open("api_test_report.html", "w", encoding="utf-8") as f:
        f.write(html_report)
    
    print(f"\n测试报告已生成：")
    print(f"  - JSON报告: api_test_report.json")
    print(f"  - HTML报告: api_test_report.html")

if __name__ == "__main__":
    run_all_tests()
