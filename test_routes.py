import sys
import os

# 将backend目录添加到Python路径
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# 测试所有注册的路由
def test_all_routes():
    print("All registered routes:")
    for route in app.routes:
        print(f"- {route.path} (methods: {route.methods})")
    
    # 测试API路由是否存在
    print("\nTesting API routes...")
    
    # 测试任务中心API（应该正常工作）
    print("\nTesting tasks API...")
    response = client.get("/api/v1/tasks")
    print(f"Tasks Response Status: {response.status_code}")
    print(f"Tasks Response: {response.text}")
    
    # 测试文件定义API
    print("\nTesting file-definitions API...")
    response = client.get("/api/v1/admin/file-definitions")
    print(f"File Definitions Response Status: {response.status_code}")
    print(f"File Definitions Response: {response.text}")
    
    # 测试字段映射API
    print("\nTesting field-pipelines API...")
    response = client.get("/api/v1/admin/field-pipelines")
    print(f"Field Pipelines Response Status: {response.status_code}")
    print(f"Field Pipelines Response: {response.text}")
    
    # 测试规则定义API
    print("\nTesting rule-definitions API...")
    response = client.get("/api/v1/admin/rule-definitions")
    print(f"Rule Definitions Response Status: {response.status_code}")
    print(f"Rule Definitions Response: {response.text}")

if __name__ == "__main__":
    test_all_routes()