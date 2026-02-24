"""
检查日志文件
"""

import os
import glob

def check_log_files():
    """检查日志文件"""
    print("=" * 100)
    print("检查日志文件")
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
        
        # 查找file_definitions相关的日志
        print(f"\nfile_definitions相关的日志:")
        for line in lines:
            if 'file_definitions' in line.lower():
                print(line.strip())
    
    print("\n" + "=" * 100)
    print("检查完成")
    print("=" * 100)

if __name__ == "__main__":
    check_log_files()
