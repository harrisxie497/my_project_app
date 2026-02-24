"""
检查test_delivery.log文件中的DEFAULT操作日志
"""

def check_test_delivery_logs():
    """检查test_delivery.log文件中的DEFAULT操作日志"""
    print("=" * 100)
    print("检查test_delivery.log文件中的DEFAULT操作日志")
    print("=" * 100)
    
    log_file = r'C:\Users\harris.xie\Documents\trae_projects\japan\backend\logs\test_delivery.log'
    
    # 读取日志文件
    with open(log_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # 查找DEFAULT操作相关的日志
    print(f"\nDEFAULT操作相关的日志:")
    default_logs = [line.strip() for line in lines if 'DEFAULT' in line or 'default' in line.lower()]
    for line in default_logs:
        print(line)
    
    # 查找处理列配置的日志
    print(f"\n处理列配置的日志:")
    config_logs = [line.strip() for line in lines if '处理列配置' in line]
    for line in config_logs:
        print(line)
    
    # 查找COPY+DEFAULT操作的日志
    print(f"\nCOPY+DEFAULT操作的日志:")
    copy_default_logs = [line.strip() for line in lines if 'COPY+DEFAULT' in line]
    for line in copy_default_logs:
        print(line)
    
    # 查找copy_equal_to的日志
    print(f"\ncopy_equal_to的日志:")
    copy_equal_to_logs = [line.strip() for line in lines if 'copy_equal_to' in line]
    for line in copy_equal_to_logs:
        print(line)
    
    print("\n" + "=" * 100)
    print("检查完成")
    print("=" * 100)

if __name__ == "__main__":
    check_test_delivery_logs()
