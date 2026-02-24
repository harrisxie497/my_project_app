"""
检查最近运行的任务类型
"""

import re

def check_task_type():
    """检查任务类型"""
    print("=" * 100)
    print("检查最近运行的任务类型")
    print("=" * 100)
    
    log_file = r"C:\Users\harris.xie\Documents\trae_projects\japan\backend\logs\app.log"
    
    with open(log_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # 查找最近的"开始处理"日志
    latest_process_lines = []
    for line in reversed(lines):
        if "开始处理" in line and "文件" in line:
            latest_process_lines.append(line.strip())
            if len(latest_process_lines) >= 5:
                break
    
    print(f"\n最近的开始处理日志:")
    for line in reversed(latest_process_lines):
        print(f"  {line}")
    
    # 查找最近的"生成结果文件"日志
    latest_generate_lines = []
    for line in reversed(lines):
        if "生成结果文件" in line:
            latest_generate_lines.append(line.strip())
            if len(latest_generate_lines) >= 5:
                break
    
    print(f"\n\n最近的生成结果文件日志:")
    for line in reversed(latest_generate_lines):
        print(f"  {line}")
    
    # 查找最近的"写入表头"日志
    latest_write_lines = []
    for line in reversed(lines):
        if "写入表头（第" in line:
            latest_write_lines.append(line.strip())
            if len(latest_write_lines) >= 5:
                break
    
    print(f"\n\n最近的写入表头日志:")
    for line in reversed(latest_write_lines):
        print(f"  {line}")
    
    print("\n" + "=" * 100)
    print("检查完成")
    print("=" * 100)

if __name__ == "__main__":
    check_task_type()
