"""
检查J、K、M列的处理日志
"""

import os
import glob

def check_jkm_columns_logs():
    """检查J、K、M列的处理日志"""
    print("=" * 100)
    print("检查J、K、M列的处理日志")
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
        
        # 查找J、K、M列相关的日志
        print(f"\nJ、K、M列相关的日志（最近100条）:")
        jkm_logs = [line.strip() for line in lines if ('处理列配置' in line and ('列名: J' in line or '列名: K' in line or '列名: M' in line))]
        for line in jkm_logs[-100:]:
            print(line)
    
    print("\n" + "=" * 100)
    print("检查完成")
    print("=" * 100)

if __name__ == "__main__":
    check_jkm_columns_logs()
