"""
检查test_delivery.log文件中的所有处理列配置日志
"""

def check_all_processing_config_logs():
    """检查test_delivery.log文件中的所有处理列配置日志"""
    print("=" * 100)
    print("检查test_delivery.log文件中的所有处理列配置日志")
    print("=" * 100)
    
    log_file = r'C:\Users\harris.xie\Documents\trae_projects\japan\backend\logs\test_delivery.log'
    
    # 读取日志文件
    with open(log_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # 查找所有处理列配置的日志
    print(f"\n所有处理列配置的日志:")
    config_logs = [line.strip() for line in lines if '处理列配置' in line]
    for line in config_logs:
        print(line)
    
    # 查找所有开始按列处理数据的日志
    print(f"\n所有开始按列处理数据的日志:")
    process_logs = [line.strip() for line in lines if '开始按列处理数据' in line]
    for line in process_logs:
        print(line)
    
    print("\n" + "=" * 100)
    print("检查完成")
    print("=" * 100)

if __name__ == "__main__":
    check_all_processing_config_logs()
