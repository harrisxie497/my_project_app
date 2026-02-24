"""
检查最新运行的任务的日志，查看写入的表头顺序
"""

import re

def check_latest_run():
    """检查最新运行的任务"""
    print("=" * 100)
    print("检查最新运行的任务的日志")
    print("=" * 100)
    
    log_file = r"C:\Users\harris.xie\Documents\trae_projects\japan\backend\logs\app.log"
    
    with open(log_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # 查找最新的"从file_definitions中获取列顺序"日志
    latest_headers_line = None
    for line in reversed(lines):
        if "从file_definitions中获取列顺序:" in line:
            latest_headers_line = line
            break
    
    if latest_headers_line:
        print(f"\n最新的从file_definitions中获取列顺序:")
        print(f"  {latest_headers_line.strip()}")
        
        # 提取表头列表
        match = re.search(r'\[.*\]', latest_headers_line)
        if match:
            headers_str = match.group(0)
            print(f"\n  表头列表: {headers_str}")
    
    # 查找最新的"写入表头"日志
    latest_write_headers_line = None
    for line in reversed(lines):
        if "写入表头（第" in line:
            latest_write_headers_line = line
            break
    
    if latest_write_headers_line:
        print(f"\n最新的写入表头:")
        print(f"  {latest_write_headers_line.strip()}")
        
        # 提取表头列表
        match = re.search(r'\[.*\]', latest_write_headers_line)
        if match:
            headers_str = match.group(0)
            print(f"\n  表头列表: {headers_str}")
    
    # 查找最新的"按列处理完成"日志
    latest_process_complete_line = None
    for line in reversed(lines):
        if "按列处理完成，处理了" in line:
            latest_process_complete_line = line
            break
    
    if latest_process_complete_line:
        print(f"\n最新的按列处理完成:")
        print(f"  {latest_process_complete_line.strip()}")
    
    # 查找最新的"处理列配置"日志
    print(f"\n\n最新的处理列配置（前10列）:")
    count = 0
    for line in reversed(lines):
        if "处理列配置 - 列名:" in line and count < 10:
            print(f"  {line.strip()}")
            count += 1
    
    print("\n" + "=" * 100)
    print("检查完成")
    print("=" * 100)

if __name__ == "__main__":
    check_latest_run()
