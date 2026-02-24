"""
检查AI批量处理的详细日志
"""

def check_ai_batch_detailed_logs():
    """检查AI批量处理的详细日志"""
    print("=" * 100)
    print("检查AI批量处理的详细日志")
    print("=" * 100)
    
    log_file = r'C:\Users\harris.xie\Documents\trae_projects\japan\backend\logs\app.log'
    
    # 读取日志文件
    with open(log_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # 查找AI批量处理的日志
    print(f"\n批量执行AI规则的日志:")
    
    # 查找"批量执行AI规则：policy_ai_text_dress_clean"的日志
    batch_indices = [idx for idx, line in enumerate(lines) if '批量执行AI规则：policy_ai_text_dress_clean' in line]
    
    if batch_indices:
        for idx in batch_indices:
            print(lines[idx].strip())
    else:
        print("未找到批量执行AI规则的日志")
    
    # 查找"解析后的结果数量"的日志
    print(f"\n解析后的结果数量日志:")
    
    result_indices = [idx for idx, line in enumerate(lines) if '解析后的结果数量' in line]
    
    if result_indices:
        for idx in result_indices[-10:]:  # 只打印最后10条
            print(lines[idx].strip())
    else:
        print("未找到解析后的结果数量的日志")
    
    # 查找"解析后的结果"的日志
    print(f"\n解析后的结果日志:")
    
    result_data_indices = [idx for idx, line in enumerate(lines) if '解析后的结果:' in line]
    
    if result_data_indices:
        for idx in result_data_indices[-5:]:  # 只打印最后5条
            print(lines[idx].strip())
    else:
        print("未找到解析后的结果的日志")
    
    print("\n" + "=" * 100)
    print("检查完成")
    print("=" * 100)

if __name__ == "__main__":
    check_ai_batch_detailed_logs()
