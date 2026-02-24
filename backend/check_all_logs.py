"""
检查最新的日志文件（全部内容）
"""

import os
import glob

def check_all_logs():
    """检查最新的日志文件（全部内容）"""
    print("=" * 100)
    print("检查最新的日志文件（全部内容）")
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
        
        # 查找最新的日志（最后500行）
        print(f"\n最新的日志（最后500行）:")
        for line in lines[-500:]:
            print(line.strip())
    
    print("\n" + "=" * 100)
    print("检查完成")
    print("=" * 100)

if __name__ == "__main__":
    check_all_logs()
