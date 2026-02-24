"""
检查日志文件中的header_params信息
"""

import os
import glob

def check_header_params_in_logs():
    """检查日志文件中的header_params信息"""
    print("=" * 100)
    print("检查日志文件中的header_params信息")
    print("=" * 100)
    
    log_dir = r'C:\Users\harris.xie\Documents\trae_projects\japan\backend\logs'
    
    # 查找最新的日志文件
    log_files = glob.glob(os.path.join(log_dir, '*.log'))
    log_files.sort(key=os.path.getmtime, reverse=True)
    
    if log_files:
        latest_log_file = log_files[0]
        print(f"\n最新的日志文件: {latest_log_file}")
        
        # 读取日志文件
        with open(latest_log_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # 查找header_params相关的日志
        print(f"\nheader_params相关的日志（最近50条）:")
        header_params_logs = [line.strip() for line in lines if 'header_params' in line]
        for line in header_params_logs[-50:]:
            print(line)
    
    print("\n" + "=" * 100)
    print("检查完成")
    print("=" * 100)

if __name__ == "__main__":
    check_header_params_in_logs()
