"""
检查test_delivery.log文件中的COPY操作日志
"""

def check_copy_operation_logs():
    """检查test_delivery.log文件中的COPY操作日志"""
    print("=" * 100)
    print("检查test_delivery.log文件中的COPY操作日志")
    print("=" * 100)
    
    log_file = r'C:\Users\harris.xie\Documents\trae_projects\japan\backend\logs\test_delivery.log'
    
    # 读取日志文件
    with open(log_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # 查找COPY操作的日志
    print(f"\nCOPY操作的日志:")
    copy_logs = [line.strip() for line in lines if 'COPY操作' in line]
    for line in copy_logs:
        print(line)
    
    # 查找J、K、M列的COPY操作日志
    print(f"\nJ、K、M列的COPY操作日志:")
    jkm_copy_logs = [line.strip() for line in lines if 'COPY操作' in line and ('target_col: J' in line or 'target_col: K' in line or 'target_col: M' in line)]
    for line in jkm_copy_logs:
        print(line)
    
    print("\n" + "=" * 100)
    print("检查完成")
    print("=" * 100)

if __name__ == "__main__":
    check_copy_operation_logs()
