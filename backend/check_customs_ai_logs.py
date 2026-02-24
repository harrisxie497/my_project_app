"""
检查CUSTOMS类型任务的AI处理日志
"""

def check_customs_ai_logs():
    """检查CUSTOMS类型任务的AI处理日志"""
    print("=" * 100)
    print("检查CUSTOMS类型任务的AI处理日志")
    print("=" * 100)
    
    log_file = r'C:\Users\harris.xie\Documents\trae_projects\japan\backend\logs\app.log'
    
    # 读取日志文件
    with open(log_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # 查找AI处理的日志
    print(f"\n批量执行AI规则的日志:")
    
    # 查找"批量执行AI规则"的日志
    batch_indices = [idx for idx, line in enumerate(lines) if '批量执行AI规则' in line]
    
    if batch_indices:
        for idx in batch_indices:
            print(lines[idx].strip())
    else:
        print("未找到批量执行AI规则的日志")
    
    # 查找"调用AI的输入数据"的日志
    print(f"\n调用AI的输入数据日志:")
    
    input_indices = [idx for idx, line in enumerate(lines) if '调用AI的输入数据' in line]
    
    if input_indices:
        for idx in input_indices[-5:]:  # 只打印最后5条
            print(lines[idx].strip())
    else:
        print("未找到调用AI的输入数据的日志")
    
    # 查找"AI返回的输出数据"的日志
    print(f"\nAI返回的输出数据日志:")
    
    output_indices = [idx for idx, line in enumerate(lines) if 'AI返回的输出数据' in line]
    
    if output_indices:
        for idx in output_indices[-5:]:  # 只打印最后5条
            print(lines[idx].strip())
    else:
        print("未找到AI返回的输出数据的日志")
    
    print("\n" + "=" * 100)
    print("检查完成")
    print("=" * 100)

if __name__ == "__main__":
    check_customs_ai_logs()
