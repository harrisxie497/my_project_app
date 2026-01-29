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

# 生成测试报告
def generate_report(tests):
    report = "# API接口测试命令\n\n"
    report += f"**生成时间**: {os.popen('powershell -Command Get-Date -Format yyyy-MM-dd_HH-mm-ss').read().strip()}\n\n"
    report += f"**接口总数**: {len(tests)}\n\n"
    
    # 按标签分组
    tag_groups = {}
    for test in tests:
        # 获取标签
        tag = test['path'].split('/')[2] if len(test['path'].split('/')) > 2 else 'other'
        if tag not in tag_groups:
            tag_groups[tag] = []
        tag_groups[tag].append(test)
    
    # 生成详细测试结果
    report += "## 详细接口列表\n\n"
    
    for tag, tag_tests in tag_groups.items():
        report += f"### {tag}\n\n"
        
        for test in tag_tests:
            report += f"#### {test['method']} {test['path']}\n"
            report += f"**摘要**: {test['summary']}\n"
            report += f"**操作ID**: {test['operation_id']}\n"
            report += f"**curl命令**:\n```bash\n{test['curl_cmd']}\n```\n\n"
    
    return report

# 主函数
def main():
    print("获取OpenAPI文档...")
    spec = get_openapi_spec()
    
    print("生成测试命令...")
    tests = generate_curl_tests(spec)
    
    print(f"共生成 {len(tests)} 个测试命令")
    
    # 生成报告
    print("\n生成测试报告...")
    report = generate_report(tests)
    
    # 保存报告
    report_file = "api_curl_commands.md"
    with open(report_file, "w", encoding="utf-8") as f:
        f.write(report)
    
    print(f"\n测试命令已保存到 {report_file}")

if __name__ == "__main__":
    main()