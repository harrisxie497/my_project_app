"""
检查最新的DELIVERY处理日志
"""

import os
import glob

def check_latest_delivery_logs():
    """检查最新的DELIVERY处理日志"""
    print("=" * 100)
    print("检查最新的DELIVERY处理日志")
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
        
        # 查找DELIVERY处理相关的日志（最后200行）
        print(f"\nDELIVERY处理相关的日志（最后200行）:")
        delivery_logs = [line.strip() for line in lines[-200:] if 'DELIVERY' in line or 'delivery_processor' in line.lower() or '按列处理' in line or '处理列配置' in line]
        for line in delivery_logs:
            print(line)
    
    print("\n" + "=" * 100)
    print("检查完成")
    print("=" * 100)

if __name__ == "__main__":
    check_latest_delivery_logs()
