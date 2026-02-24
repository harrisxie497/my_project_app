"""
检查test_delivery.log文件中的field_type日志
"""

def check_field_type_logs():
    """检查test_delivery.log文件中的field_type日志"""
    print("=" * 100)
    print("检查test_delivery.log文件中的field_type日志")
    print("=" * 100)
    
    log_file = r'C:\Users\harris.xie\Documents\trae_projects\japan\backend\logs\test_delivery.log'
    
    # 读取日志文件
    with open(log_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # 查找field_type为DEFAULT的日志
    print(f"\nfield_type为DEFAULT的日志:")
    default_type_logs = [line.strip() for line in lines if 'field_type: DEFAULT' in line]
    for line in default_type_logs[:10]:
        print(line)
    
    # 查找COPY+DEFAULT操作的日志
    print(f"\nCOPY+DEFAULT操作的日志:")
    copy_default_logs = [line.strip() for line in lines if 'COPY+DEFAULT操作' in line]
    for line in copy_default_logs:
        print(line)
    
    print("\n" + "=" * 100)
    print("检查完成")
    print("=" * 100)

if __name__ == "__main__":
    check_field_type_logs()
