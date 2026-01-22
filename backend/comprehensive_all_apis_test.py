import requests
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

# 登录获取令牌
def login():
    url = f"{BASE_URL}/auth/login"
    data = {
        "username": TEST_USERNAME,
        "password": TEST_PASSWORD
    }
    response = test_post_request("1.1 登录接口", url, None, data=data)
    if response and response.get("ok"):
        return response["data"]["access_token"]
    return None

# 认证相关API测试
def test_auth_apis(token):
    print("\n=== 1. 认证相关API ===")
    # 测试获取当前用户信息
    test_get_request("1.2 获取当前用户信息", f"{BASE_URL}/auth/me", token)
    
    # 测试登出接口
    test_post_request("1.3 登出接口", f"{BASE_URL}/auth/logout", token)

# 任务管理API测试
def test_task_apis(token):
    print("\n=== 2. 任务管理API ===")
    # 测试获取任务列表
    test_get_request("2.1 获取任务列表", f"{BASE_URL}/tasks", token)
    
    # 测试获取任务详情（使用不存在的ID，预期404）
    test_get_request("2.2 获取任务详情（不存在）", f"{BASE_URL}/tasks/not_exist", token, expected_status=404)
    
    # 测试获取任务对比统计（使用不存在的ID，预期404）
    test_get_request("2.3 获取任务对比统计", f"{BASE_URL}/tasks/not_exist/stats", token, expected_status=404)
    
    # 测试下载任务文件（使用不存在的ID，预期404）
    test_get_request("2.4 下载任务文件", f"{BASE_URL}/tasks/not_exist/files/original", token, expected_status=404)

# 规则表管理API测试
def test_rule_table_apis(token):
    print("\n=== 3. 规则表管理API ===")
    # 测试获取规则表列表
    test_get_request("3.1 获取规则表列表", f"{BASE_URL}/rule-tables", token)
    
    # 测试获取规则表详情（使用不存在的ID，预期404）
    test_get_request("3.2 获取规则表详情", f"{BASE_URL}/rule-tables/not_exist", token, expected_status=404)
    
    # 测试启用规则表（使用不存在的ID，预期404）
    test_put_request("3.3 启用规则表", f"{BASE_URL}/rule-tables/not_exist/enable", token, expected_status=404)
    
    # 测试禁用规则表（使用不存在的ID，预期404）
    test_put_request("3.4 禁用规则表", f"{BASE_URL}/rule-tables/not_exist/disable", token, expected_status=404)
    
    # 管理员获取规则表列表
    test_get_request("3.5 管理员获取规则表列表", f"{BASE_URL}/admin/rule-tables", token)

# 规则项管理API测试
def test_rule_item_apis(token):
    print("\n=== 4. 规则项管理API ===")
    # 测试获取规则项列表
    test_get_request("4.1 获取规则项列表", f"{BASE_URL}/rule-items", token)
    
    # 测试获取规则项详情（使用不存在的ID，预期404）
    test_get_request("4.2 获取规则项详情", f"{BASE_URL}/rule-items/not_exist", token, expected_status=404)
    
    # 测试启用规则项（使用不存在的ID，预期404）
    test_put_request("4.3 启用规则项", f"{BASE_URL}/rule-items/not_exist/enable", token, expected_status=404)
    
    # 测试禁用规则项（使用不存在的ID，预期404）
    test_put_request("4.4 禁用规则项", f"{BASE_URL}/rule-items/not_exist/disable", token, expected_status=404)
    
    # 测试获取指定规则表的规则项（使用不存在的ID，预期404）
    test_get_request("4.5 获取指定规则表的规则项", f"{BASE_URL}/rule-items/rule-table/not_exist", token, expected_status=404)
    
    # 管理员获取规则表的规则项（使用不存在的ID，预期404）
    test_get_request("4.6 管理员获取规则表的规则项", f"{BASE_URL}/admin/rule-tables/not_exist/items", token, expected_status=404)
    
    # 测试规则导入接口（文件上传）
    test_file_path = "test_rules.xlsx"
    with open(test_file_path, "w") as f:
        f.write("PK\x03\x04")  # 简单的ZIP文件头，模拟空Excel文件
    
    try:
        with open(test_file_path, "rb") as f:
            files = {"file": (test_file_path, f, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")}
            test_post_request("4.7 规则导入", f"{BASE_URL}/admin/rules/import", token, files=files)
    except Exception as e:
        print_test_result("4.7 规则导入", "FAILED", str(e))
    finally:
        if os.path.exists(test_file_path):
            os.remove(test_file_path)

# 模板映射管理API测试
def test_template_mapping_apis(token):
    print("\n=== 5. 模板映射管理API ===")
    # 测试获取模板映射列表
    test_get_request("5.1 获取模板映射列表", f"{BASE_URL}/template-mappings", token)
    
    # 测试获取模板映射详情（使用不存在的ID，预期404）
    test_get_request("5.2 获取模板映射详情", f"{BASE_URL}/template-mappings/not_exist", token, expected_status=404)
    
    # 测试启用模板映射（使用不存在的ID，预期404）
    test_put_request("5.3 启用模板映射", f"{BASE_URL}/template-mappings/not_exist/enable", token, expected_status=404)
    
    # 测试禁用模板映射（使用不存在的ID，预期404）
    test_put_request("5.4 禁用模板映射", f"{BASE_URL}/template-mappings/not_exist/disable", token, expected_status=404)
    
    # 管理员获取模板映射列表
    test_get_request("5.5 管理员获取模板映射列表", f"{BASE_URL}/admin/template-mappings", token)
    
    # 模板映射自检（使用不存在的ID，预期404）
    test_post_request("5.6 模板映射自检", f"{BASE_URL}/admin/template-mappings/not_exist/validate", token, expected_status=404)

# AI字段能力管理API测试
def test_ai_capability_apis(token):
    print("\n=== 6. AI字段能力管理API ===")
    # 测试获取AI字段能力列表
    test_get_request("6.1 获取AI字段能力列表", f"{BASE_URL}/ai-capabilities", token)
    
    # 测试获取AI字段能力详情（使用不存在的ID，预期404）
    test_get_request("6.2 获取AI字段能力详情", f"{BASE_URL}/ai-capabilities/not_exist", token, expected_status=404)
    
    # 测试启用AI字段能力（使用不存在的ID，预期404）
    test_put_request("6.3 启用AI字段能力", f"{BASE_URL}/ai-capabilities/not_exist/enable", token, expected_status=404)
    
    # 测试禁用AI字段能力（使用不存在的ID，预期404）
    test_put_request("6.4 禁用AI字段能力", f"{BASE_URL}/ai-capabilities/not_exist/disable", token, expected_status=404)
    
    # 管理员获取AI字段能力列表
    test_get_request("6.5 管理员获取AI字段能力列表", f"{BASE_URL}/admin/ai-capabilities", token)

# Excel配置管理API测试
def test_excel_config_apis(token):
    print("\n=== 7. Excel配置管理API ===")
    # 测试获取当前Excel配置
    test_get_request("7.1 获取当前Excel配置", f"{BASE_URL}/admin/excel-configs/active?file_type=customs", token, expected_status=404)  # 预期404，因为还没有配置
    
    # 测试获取Excel配置列表
    test_get_request("7.2 获取Excel配置列表", f"{BASE_URL}/excel-configs", token)
    
    # 测试获取Excel配置详情（使用不存在的ID，预期404）
    test_get_request("7.3 获取Excel配置详情", f"{BASE_URL}/excel-configs/not_exist", token, expected_status=404)

# 用户管理API测试
def test_user_apis(token):
    print("\n=== 8. 用户管理API ===")
    # 测试获取用户列表
    test_get_request("8.1 获取用户列表", f"{BASE_URL}/users", token)
    
    # 测试获取用户详情（使用不存在的ID，预期404）
    test_get_request("8.2 获取用户详情", f"{BASE_URL}/users/not_exist", token, expected_status=404)
    
    # 测试启用用户（使用不存在的ID，预期404）
    test_put_request("8.3 启用用户", f"{BASE_URL}/users/not_exist/enable", token, expected_status=404)
    
    # 测试禁用用户（使用不存在的ID，预期404）
    test_put_request("8.4 禁用用户", f"{BASE_URL}/users/not_exist/disable", token, expected_status=404)
    
    # 管理员获取用户列表
    test_get_request("8.5 管理员获取用户列表", f"{BASE_URL}/admin/users", token)

# 操作日志API测试
def test_operation_log_apis(token):
    print("\n=== 9. 操作日志API ===")
    # 测试获取操作日志列表
    test_get_request("9.1 获取操作日志列表", f"{BASE_URL}/operation-logs", token)
    
    # 测试获取操作日志详情（使用不存在的ID，预期404）
    test_get_request("9.2 获取操作日志详情", f"{BASE_URL}/operation-logs/not_exist", token, expected_status=404)
    
    # 测试获取指定用户的操作日志（使用不存在的ID，预期空列表）
    test_get_request("9.3 获取指定用户的操作日志", f"{BASE_URL}/operation-logs/user/not_exist", token)
    
    # 测试获取指定操作的日志（使用不存在的操作，预期空列表）
    test_get_request("9.4 获取指定操作的日志", f"{BASE_URL}/operation-logs/action/not_exist", token)
    
    # 管理员查询操作日志
    test_get_request("9.5 管理员查询操作日志", f"{BASE_URL}/admin/operation-logs", token)

# 主测试函数
def run_all_tests():
    print("开始执行所有API测试...")
    print(f"测试目标: {BASE_URL}")
    print(f"测试用户: {TEST_USERNAME}")
    print("=" * 60)
    
    # 1. 登录获取令牌
    token = login()
    if not token:
        print("\n❌ 登录失败，无法继续测试")
        return
    
    # 2. 执行其他测试
    test_auth_apis(token)
    test_task_apis(token)
    test_rule_table_apis(token)
    test_rule_item_apis(token)
    test_template_mapping_apis(token)
    test_ai_capability_apis(token)
    test_excel_config_apis(token)
    test_user_apis(token)
    test_operation_log_apis(token)
    
    # 3. 打印测试总结
    print("\n" + "=" * 60)
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
    with open("api_all_tests_report.json", "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    # 生成HTML报告
    html_report = f"""
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>API全面测试报告</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; }}
            .header {{ background: #f0f0f0; padding: 10px; border-radius: 5px; margin-bottom: 20px; }}
            .summary {{ margin: 20px 0; }}
            .status {{ font-weight: bold; }}
            .passed {{ color: green; }}
            .failed {{ color: red; }}
            .error-list {{ margin-top: 20px; }}
            .error-item {{ background: #ffebee; padding: 10px; margin: 5px 0; border-radius: 3px; }}
            .section {{ margin: 30px 0; }}
            .section-title {{ font-size: 18px; font-weight: bold; margin-bottom: 10px; color: #333; }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>API全面测试报告</h1>
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
        
        <div class="section">
            <div class="section-title">错误详情</div>
            <div class="error-list">
                {''.join([f'<div class="error-item">{error}</div>' for error in report['errors']]) if report['errors'] else '<p>没有错误</p>'}
            </div>
        </div>
        
        <div class="section">
            <div class="section-title">测试覆盖率</div>
            <p>已测试API数量: {report['results']['total']}</p>
            <p>设计文档API数量: 75</p>
            <p>覆盖率: {report['results']['total']/75*100:.1f}%</p>
        </div>
    </body>
    </html>
    """
    
    with open("api_all_tests_report.html", "w", encoding="utf-8") as f:
        f.write(html_report)
    
    print(f"\n测试报告已生成：")
    print(f"  - JSON报告: api_all_tests_report.json")
    print(f"  - HTML报告: api_all_tests_report.html")

if __name__ == "__main__":
    run_all_tests()
