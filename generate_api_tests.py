import json
import requests
import os

# 获取OpenAPI文档
def get_openapi_spec():
    response = requests.get("http://127.0.0.1:8000/openapi.json")
    response.raise_for_status()
    return response.json()

# 生成curl测试命令
def generate_curl_tests(spec):
    tests = []
    base_url = "http://127.0.0.1:8000"
    
    # 遍历所有路径
    for path, path_info in spec["paths"].items():
        # 遍历所有HTTP方法
        for method, method_info in path_info.items():
            # 跳过OPTIONS和HEAD方法
            if method in ["options", "head"]:
                continue
            
            # 构建完整URL
            url = base_url + path
            
            # 获取操作ID和摘要
            operation_id = method_info.get("operationId", "")
            summary = method_info.get("summary", "")
            
            # 生成curl命令
            curl_cmd = f"curl -X {method.upper()} \"{url}\" -H \"accept: application/json\""
            
            # 如果是POST或PUT，添加默认的Content-Type头
            if method in ["post", "put", "patch"]:
                curl_cmd += " -H \"Content-Type: application/json\""
                
                # 检查是否有请求体示例
                if "requestBody" in method_info:
                    media_type = list(method_info["requestBody"]["content"].keys())[0]
                    if "example" in method_info["requestBody"]["content"][media_type]:
                        example = method_info["requestBody"]["content"][media_type]["example"]
                        # 将示例转换为JSON字符串
                        example_json = json.dumps(example)
                        curl_cmd += f" -d \"{example_json}\""
                    elif "examples" in method_info["requestBody"]["content"][media_type]:
                        # 使用第一个示例
                        first_example_key = list(method_info["requestBody"]["content"][media_type]["examples"].keys())[0]
                        example = method_info["requestBody"]["content"][media_type]["examples"][first_example_key]["value"]
                        example_json = json.dumps(example)
                        curl_cmd += f" -d \"{example_json}\""
                    else:
                        # 添加空请求体
                        curl_cmd += " -d \"{}\""
            
            # 添加到测试列表
            tests.append({
                "method": method.upper(),
                "path": path,
                "operation_id": operation_id,
                "summary": summary,
                "curl_cmd": curl_cmd
            })
    
    return tests

# 执行测试并记录结果
def run_tests(tests):
    results = []
    
    for test in tests:
        print(f"\nTesting {test['method']} {test['path']}...")
        print(f"Summary: {test['summary']}")
        print(f"Command: {test['curl_cmd']}")
        
        # 在PowerShell中执行curl命令
        try:
            # 直接使用curl命令，而不是Invoke-RestMethod
            # 在PowerShell中需要使用--%来停止解析
            powershell_cmd = f"curl --% {test['curl_cmd']}"
            
            # 执行命令
            result = os.popen(f"powershell -Command \"{powershell_cmd}\"")
            output = result.read()
            exit_code = result.close()
            
            # 记录结果
            results.append({
                **test,
                "output": output,
                "exit_code": exit_code or 0
            })
            
            print(f"Exit Code: {exit_code or 0}")
            print(f"Output: {output[:200]}..." if len(output) > 200 else f"Output: {output}")
            
        except Exception as e:
            results.append({
                **test,
                "output": str(e),
                "exit_code": 1
            })
            print(f"Error: {e}")
    
    return results

# 生成测试报告
def generate_report(tests, results):
    report = "# API接口测试报告\n\n"
    report += f"**测试时间**: {os.popen('powershell -Command Get-Date -Format yyyy-MM-dd_HH-mm-ss').read().strip()}\n\n"
    report += f"**测试总数**: {len(tests)}\n"
    report += f"**成功数**: {sum(1 for r in results if r['exit_code'] == 0)}\n"
    report += f"**失败数**: {sum(1 for r in results if r['exit_code'] != 0)}\n\n"
    
    # 按标签分组
    tag_groups = {}
    for test in tests:
        # 获取标签
        tags = []
        # 这里简化处理，实际应该从spec中获取标签
        tag = test['path'].split('/')[2] if len(test['path'].split('/')) > 2 else 'other'
        if tag not in tag_groups:
            tag_groups[tag] = []
        tag_groups[tag].append(test)
    
    # 生成详细测试结果
    report += "## 详细测试结果\n\n"
    
    for tag, tag_tests in tag_groups.items():
        report += f"### {tag}\n\n"
        
        for test in tag_tests:
            # 查找对应的结果
            result = next(r for r in results if r['path'] == test['path'] and r['method'] == test['method'])
            status = "✅ 成功" if result['exit_code'] == 0 else "❌ 失败"
            
            report += f"#### {status} {test['method']} {test['path']}\n"
            report += f"**摘要**: {test['summary']}\n"
            report += f"**操作ID**: {test['operation_id']}\n"
            report += f"**命令**: `{test['curl_cmd']}`\n"
            report += f"**退出码**: {result['exit_code']}\n"
            report += f"**输出**:\n```\n{result['output']}\n```\n\n"
    
    return report

# 主函数
def main():
    print("获取OpenAPI文档...")
    spec = get_openapi_spec()
    
    print("生成测试命令...")
    tests = generate_curl_tests(spec)
    
    print(f"共生成 {len(tests)} 个测试命令")
    
    # 执行测试
    print("\n执行测试...")
    results = run_tests(tests)
    
    # 生成报告
    print("\n生成测试报告...")
    report = generate_report(tests, results)
    
    # 保存报告
    report_file = "api_test_report.md"
    with open(report_file, "w", encoding="utf-8") as f:
        f.write(report)
    
    print(f"\n测试完成！报告已保存到 {report_file}")
    
    # 也保存为HTML格式
    html_report = f"<!DOCTYPE html>\n<html>\n<head>\n    <meta charset='utf-8'>\n    <title>API测试报告</title>\n    <style>\n        body {{ font-family: Arial, sans-serif; margin: 20px; }} \n        h1, h2, h3, h4 {{ color: #333; }} \n        code {{ background-color: #f4f4f4; padding: 2px 4px; border-radius: 4px; }} \n        pre {{ background-color: #f4f4f4; padding: 10px; border-radius: 4px; overflow-x: auto; }} \n        .success {{ color: green; }} \n        .failure {{ color: red; }} \n        .test-item {{ margin-bottom: 20px; padding: 10px; border: 1px solid #ddd; border-radius: 4px; }} \n        .test-header {{ font-weight: bold; margin-bottom: 5px; }} \n    </style>\n</head>\n<body>\n{report.replace('\n', '<br>').replace('```', '<pre>').replace('**', '<b>').replace('</b>', '</b>')}\n</body>\n</html>"
    
    with open("api_test_report.html", "w", encoding="utf-8") as f:
        f.write(html_report)
    
    print(f"HTML报告已保存到 api_test_report.html")

if __name__ == "__main__":
    main()