import openpyxl
import os

# 创建测试Excel文件
def create_test_excel():
    """创建一个简单的测试Excel文件"""
    # 创建工作簿
    wb = openpyxl.Workbook()
    
    # 获取活跃工作表
    ws = wb.active
    ws.title = "测试数据"
    
    # 添加表头
    headers = ["商品名称", "数量", "单价", "金额", "HS编码", "原产国"]
    ws.append(headers)
    
    # 添加测试数据
    test_data = [
        ["测试商品1", 10, 100, 1000, "8471.3000", "中国"],
        ["测试商品2", 5, 200, 1000, "8528.7200", "日本"],
        ["测试商品3", 20, 50, 1000, "9013.8030", "美国"]
    ]
    
    for row in test_data:
        ws.append(row)
    
    # 保存文件
    file_path = "test_task_file.xlsx"
    wb.save(file_path)
    print(f"已创建测试Excel文件: {file_path}")
    return file_path

if __name__ == "__main__":
    create_test_excel()