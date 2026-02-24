"""
检查CUSTOMS类型任务的AI批量处理日志
"""

def check_customs_ai_batch_logs():
    """检查CUSTOMS类型任务的AI批量处理日志"""
    print("=" * 100)
    print("检查CUSTOMS类型任务的AI批量处理日志")
    print("=" * 100)
    
    log_file = r'C:\Users\harris.xie\Documents\trae_projects\japan\backend\logs\app.log'
    
    # 读取日志文件
    with open(log_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # 查找批量处理收件人地址的日志
    print(f"\n批量处理收件人地址的日志:")
    
    # 查找"开始批量处理收件人地址清理和翻译"的日志
    start_indices = [idx for idx, line in enumerate(lines) if '开始批量处理收件人地址清理和翻译' in line]
    
    if start_indices:
        start_idx = start_indices[-1]  # 使用最后一次
        # 打印从开始到结束的所有日志
        for idx in range(start_idx, min(start_idx + 200, len(lines))):
            print(lines[idx].strip())
    else:
        print("未找到批量处理收件人地址的日志")
    
    print("\n" + "=" * 100)
    print("检查完成")
    print("=" * 100)

if __name__ == "__main__":
    check_customs_ai_batch_logs()
