"""
检查test_delivery.log文件中的处理列配置日志
"""

def check_processing_config_logs():
    """检查test_delivery.log文件中的处理列配置日志"""
    print("=" * 100)
    print("检查test_delivery.log文件中的处理列配置日志")
    print("=" * 100)
    
    log_file = r'C:\Users\harris.xie\Documents\trae_projects\japan\backend\logs\test_delivery.log'
    
    # 读取日志文件
    with open(log_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # 查找J、K、M列的处理列配置日志
    print(f"\nJ、K、M列的处理列配置日志:")
    jkm_config_logs = [line.strip() for line in lines if '处理列配置' in line and ('列名: J' in line or '列名: K' in line or '列名: M' in line)]
    for line in jkm_config_logs:
        print(line)
    
    # 查找COPY+DEFAULT操作的日志
    print(f"\nCOPY+DEFAULT操作的日志:")
    copy_default_logs = [line.strip() for line in lines if 'COPY+DEFAULT操作' in line]
    for line in copy_default_logs:
        print(line)
    
    # 查找依頼主、依頼主住所、依頼主電話列的处理日志
    print(f"\n依頼主、依頼主住所、依頼主電話列的处理日志:")
    default_col_logs = [line.strip() for line in lines if '依頼主' in line]
    for line in default_col_logs:
        print(line)
    
    print("\n" + "=" * 100)
    print("检查完成")
    print("=" * 100)

if __name__ == "__main__":
    check_processing_config_logs()
