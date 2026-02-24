"""
检查最新运行中处理了哪些列
"""

import re

def check_latest_run_columns():
    """检查最新运行中处理了哪些列"""
    print("=" * 100)
    print("检查最新运行中处理了哪些列")
    print("=" * 100)
    
    # 读取日志文件
    log_file_path = r'C:\Users\harris.xie\Documents\trae_projects\japan\backend\logs\app.log'
    
    with open(log_file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # 找到最新的"解析原始文件"日志
    start_idx = -1
    for i in range(len(lines) - 1, -1, -1):
        if "解析原始文件" in lines[i]:
            start_idx = i
            break
    
    if start_idx == -1:
        print("❌ 没有找到'解析原始文件'日志")
        return
    
    print(f"\n从第{start_idx}行开始查找处理列配置记录:")
    
    # 查找所有"处理列配置"记录
    processed_columns = []
    for i in range(start_idx, len(lines)):
        line = lines[i]
        match = re.search(r'处理列配置 - 列名: ([A-Z]+),', line)
        if match:
            col = match.group(1)
            if col not in processed_columns:
                processed_columns.append(col)
    
    print(f"\n处理了 {len(processed_columns)} 个列:")
    for col in processed_columns:
        print(f"  {col}")
    
    print("\n" + "=" * 100)
    print("检查完成！")
    print("=" * 100)

if __name__ == "__main__":
    check_latest_run_columns()
